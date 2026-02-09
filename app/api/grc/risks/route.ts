import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'

export async function GET(request: NextRequest) {
    try {
        const session = await auth()

        if (!session?.user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        // TODO: Fetch from database when Prisma client is regenerated
        // const risks = await prisma.risk.findMany({
        //   orderBy: { createdAt: 'desc' }
        // })

        // Return mock data
        const risks = [
            {
                id: '1',
                riskId: 'RISK-001',
                category: 'MODEL_RISK',
                description: 'ML model drift causing degraded prediction accuracy',
                likelihood: 'MEDIUM',
                impact: 'HIGH',
                riskLevel: 'HIGH',
                mitigation: 'Automated model monitoring, monthly retraining',
                owner: 'ML Engineering Team',
                status: 'MITIGATED',
            },
            {
                id: '2',
                riskId: 'RISK-002',
                category: 'COMPLIANCE_RISK',
                description: 'Non-compliance with GDPR data retention policies',
                likelihood: 'LOW',
                impact: 'CRITICAL',
                riskLevel: 'MEDIUM',
                mitigation: 'Automated data deletion after 7 years, audit logs',
                owner: 'Compliance Team',
                status: 'MONITORING',
            },
        ]

        return NextResponse.json({ risks })

    } catch (error) {
        console.error('Error fetching risks:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
