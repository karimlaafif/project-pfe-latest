import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'

export async function GET(request: NextRequest) {
    try {
        const session = await auth()

        if (!session?.user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // TODO: Fetch from database when Prisma client is regenerated
        // const frameworks = await prisma.complianceFramework.findMany({
        //   orderBy: { createdAt: 'desc' }
        // })

        // Return mock data
        const frameworks = [
            {
                id: '1',
                name: 'GDPR (General Data Protection Regulation)',
                status: 'COMPLIANT',
                completion: 100,
                lastAudit: new Date('2024-12-01'),
                nextAudit: new Date('2025-06-01'),
                findings: 0,
            },
            {
                id: '2',
                name: 'SOC 2 Type II',
                status: 'IN_PROGRESS',
                completion: 85,
                lastAudit: new Date('2024-11-15'),
                nextAudit: new Date('2025-05-15'),
                findings: 3,
            },
            {
                id: '3',
                name: 'ISO 27001 (Information Security)',
                status: 'COMPLIANT',
                completion: 98,
                lastAudit: new Date('2024-11-20'),
                nextAudit: new Date('2025-11-20'),
                findings: 1,
            },
        ]

        return NextResponse.json({ frameworks })

    } catch (error) {
        console.error('Error fetching compliance frameworks:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
