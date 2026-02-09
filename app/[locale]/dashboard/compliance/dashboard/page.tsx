'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { CheckCircle, AlertCircle, Clock, FileCheck } from 'lucide-react'

const regulations = [
    {
        name: 'GDPR (General Data Protection Regulation)',
        status: 'Compliant',
        completion: 100,
        lastAudit: '2024-12-01',
        nextAudit: '2025-06-01',
        findings: 0
    },
    {
        name: 'SOC 2 Type II',
        status: 'In Progress',
        completion: 85,
        lastAudit: '2024-11-15',
        nextAudit: '2025-05-15',
        findings: 3
    },
    {
        name: 'PCI DSS (Payment Card Industry)',
        status: 'Compliant',
        completion: 100,
        lastAudit: '2024-12-10',
        nextAudit: '2025-12-10',
        findings: 0
    },
    {
        name: 'ISO 27001 (Information Security)',
        status: 'Compliant',
        completion: 98,
        lastAudit: '2024-11-20',
        nextAudit: '2025-11-20',
        findings: 1
    },
    {
        name: 'Fair Lending Act (ECOA)',
        status: 'Compliant',
        completion: 100,
        lastAudit: '2024-12-05',
        nextAudit: '2025-06-05',
        findings: 0
    },
    {
        name: 'Basel III (Credit Risk Standards)',
        status: 'In Progress',
        completion: 75,
        lastAudit: '2024-10-30',
        nextAudit: '2025-04-30',
        findings: 5
    }
]

export default function CompliancePage() {
    const compliantCount = regulations.filter(r => r.status === 'Compliant').length
    const totalFindings = regulations.reduce((sum, r) => sum + r.findings, 0)

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Compliance Dashboard</h1>
                <p className="text-muted-foreground">Monitor regulatory compliance and audit status</p>
            </div>

            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Compliant</CardTitle>
                        <CheckCircle className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{compliantCount}/{regulations.length}</div>
                        <p className="text-xs text-muted-foreground">
                            {((compliantCount / regulations.length) * 100).toFixed(0)}% compliance rate
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Open Findings</CardTitle>
                        <AlertCircle className="h-4 w-4 text-orange-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalFindings}</div>
                        <p className="text-xs text-muted-foreground">Across all frameworks</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Audits Due</CardTitle>
                        <Clock className="h-4 w-4 text-blue-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">3</div>
                        <p className="text-xs text-muted-foreground">Next 90 days</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Certifications</CardTitle>
                        <FileCheck className="h-4 w-4 text-purple-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{compliantCount}</div>
                        <p className="text-xs text-muted-foreground">Active certifications</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Regulatory Frameworks</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-6">
                        {regulations.map((reg, index) => (
                            <div key={index} className="space-y-2">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <h3 className="font-semibold text-foreground">{reg.name}</h3>
                                        <Badge variant={reg.status === 'Compliant' ? 'default' : 'secondary'}>
                                            {reg.status}
                                        </Badge>
                                        {reg.findings > 0 && (
                                            <Badge variant="destructive">{reg.findings} findings</Badge>
                                        )}
                                    </div>
                                    <span className="text-sm font-medium text-foreground">{reg.completion}%</span>
                                </div>
                                <Progress value={reg.completion} className="h-2" />
                                <div className="flex justify-between text-sm text-muted-foreground">
                                    <span>Last Audit: {reg.lastAudit}</span>
                                    <span>Next Audit: {reg.nextAudit}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
