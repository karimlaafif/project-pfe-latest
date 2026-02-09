'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { AlertTriangle, TrendingUp, Shield } from 'lucide-react'

const risks = [
    {
        id: 'RISK-001',
        category: 'Model Risk',
        description: 'ML model drift causing degraded prediction accuracy',
        likelihood: 'Medium',
        impact: 'High',
        riskLevel: 'High',
        mitigation: 'Automated model monitoring, monthly retraining',
        owner: 'ML Engineering Team',
        status: 'Mitigated'
    },
    {
        id: 'RISK-002',
        category: 'Compliance Risk',
        description: 'Non-compliance with GDPR data retention policies',
        likelihood: 'Low',
        impact: 'Critical',
        riskLevel: 'Medium',
        mitigation: 'Automated data deletion after 7 years, audit logs',
        owner: 'Compliance Team',
        status: 'Monitoring'
    },
    {
        id: 'RISK-003',
        category: 'Fraud Risk',
        description: 'Sophisticated fraud patterns bypassing detection',
        likelihood: 'Medium',
        impact: 'High',
        riskLevel: 'High',
        mitigation: 'Ensemble fraud models, human review for high-risk cases',
        owner: 'Fraud Prevention Team',
        status: 'Active'
    },
    {
        id: 'RISK-004',
        category: 'Operational Risk',
        description: 'API downtime affecting loan processing',
        likelihood: 'Low',
        impact: 'High',
        riskLevel: 'Medium',
        mitigation: 'Multi-region deployment, auto-scaling, 99.9% SLA',
        owner: 'DevOps Team',
        status: 'Mitigated'
    },
    {
        id: 'RISK-005',
        category: 'Bias Risk',
        description: 'AI model showing demographic bias in decisions',
        likelihood: 'Medium',
        impact: 'Critical',
        riskLevel: 'High',
        mitigation: 'Fairness metrics monitoring, bias testing, explainable AI',
        owner: 'AI Ethics Committee',
        status: 'Monitoring'
    }
]

const getRiskColor = (level: string) => {
    switch (level) {
        case 'Critical': return 'text-red-500'
        case 'High': return 'text-orange-500'
        case 'Medium': return 'text-yellow-500'
        case 'Low': return 'text-green-500'
        default: return 'text-muted-foreground'
    }
}

export default function RiskRegisterPage() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Risk Register</h1>
                <p className="text-muted-foreground">Identify, assess, and manage organizational risks</p>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Critical Risks</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-red-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {risks.filter(r => r.riskLevel === 'Critical' || r.riskLevel === 'High').length}
                        </div>
                        <p className="text-xs text-muted-foreground">Requiring immediate attention</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Mitigated</CardTitle>
                        <Shield className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {risks.filter(r => r.status === 'Mitigated').length}
                        </div>
                        <p className="text-xs text-muted-foreground">Controls in place</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Trending</CardTitle>
                        <TrendingUp className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">↓ 12%</div>
                        <p className="text-xs text-muted-foreground">Risk exposure vs last quarter</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Active Risks</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {risks.map((risk) => (
                            <div key={risk.id} className="p-4 border border-border rounded-lg bg-card">
                                <div className="flex items-start justify-between">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2 mb-2">
                                            <span className="font-mono text-sm text-muted-foreground">{risk.id}</span>
                                            <Badge>{risk.category}</Badge>
                                            <Badge variant="outline" className={getRiskColor(risk.riskLevel)}>
                                                {risk.riskLevel} Risk
                                            </Badge>
                                        </div>
                                        <h3 className="font-semibold mb-1 text-foreground">{risk.description}</h3>
                                        <div className="grid grid-cols-2 gap-4 text-sm text-muted-foreground mt-3">
                                            <div>
                                                <span className="font-medium">Likelihood:</span> {risk.likelihood}
                                            </div>
                                            <div>
                                                <span className="font-medium">Impact:</span> {risk.impact}
                                            </div>
                                            <div>
                                                <span className="font-medium">Owner:</span> {risk.owner}
                                            </div>
                                            <div>
                                                <span className="font-medium">Status:</span> {risk.status}
                                            </div>
                                        </div>
                                        <div className="mt-3 p-3 bg-blue-500/10 border border-blue-500/20 rounded">
                                            <span className="text-sm font-medium text-foreground">Mitigation: </span>
                                            <span className="text-sm text-muted-foreground">{risk.mitigation}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
