
import { PrismaClient } from '@prisma/client'
import bcrypt from 'bcryptjs'

const prisma = new PrismaClient()

async function main() {
    const users = await prisma.user.findMany({ take: 5 })
    console.log(`Found ${users.length} users in total.`)
    if (users.length > 0) {
        console.log('Existing users:')
        users.forEach(u => console.log(`- ${u.email} (${u.role})`))
    } else {
        console.log('No users found in database.')
    }

    const email = 'user@test.com'
    const user = await prisma.user.findUnique({ where: { email } })

    if (!user) {
        console.log(`Creating user: ${email}`)
        const hashedPassword = await bcrypt.hash('password123', 10)

        await prisma.user.create({
            data: {
                email,
                password: hashedPassword,
                name: 'Test User',
                role: 'USER',
                emailVerified: new Date(),
            }
        })
        console.log('User created with password: password123')
    } else {
        console.log('User already exists (this should not happen based on previous check).')
    }
}

main()
    .catch((e) => {
        console.error(e)
        process.exit(1)
    })
    .finally(async () => {
        await prisma.$disconnect()
    })
