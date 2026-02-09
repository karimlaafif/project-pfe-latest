import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { prisma } from '@/lib/db'

export async function GET(request: NextRequest) {
    try {
        const session = await auth()

        if (!session?.user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // TODO: Fetch from database when Prisma client is regenerated
        // const policies = await prisma.policy.findMany({
        //   orderBy: { createdAt: 'desc' }
        // })

        // For now, return mock data
        const policies = [
            {
                id: '1',
                name: 'Data Privacy Policy (GDPR)',
                version: 'v2.1',
                status: 'ACTIVE',
                category: 'Data Protection',
                owner: 'Compliance Team',
                lastReview: new Date('2024-12-15'),
                nextReview: new Date('2025-06-15'),
            },
            {
                id: '2',
                name: 'AI Model Governance Policy',
                version: 'v1.5',
                status: 'ACTIVE',
                category: 'AI Ethics',
                owner: 'ML Team',
                lastReview: new Date('2024-11-30'),
                nextReview: new Date('2025-05-30'),
            },
        ]

        return NextResponse.json({ policies })

    } catch (error) {
        console.error('Error fetching policies:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}

export async function POST(request: NextRequest) {
    try {
        const session = await auth()

        if (!session?.user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const data = await request.json()

        // TODO: Create policy in database
        // const policy = await prisma.policy.create({
        //   data: {
        //     name: data.name,
        //     version: data.version,
        //     status: data.status,
        //     category: data.category,
        //     content: data.content,
        //     owner: data.owner,
        //     lastReview: new Date(data.lastReview),
        //     nextReview: new Date(data.nextReview),
        //   }
        // })

        return NextResponse.json({
            success: true,
            message: 'Policy created successfully'
        })

    } catch (error) {
        console.error('Error creating policy:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
