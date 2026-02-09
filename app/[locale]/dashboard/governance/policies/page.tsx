'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { FileText, CheckCircle, AlertTriangle, Clock } from 'lucide-react'

const policies = [
    {
        id: 1,
        name: 'Data Privacy Policy (GDPR)',
        version: 'v2.1',
        status: 'Active',
        lastReview: '2024-12-15',
        nextReview: '2025-06-15',
        owner: 'Compliance Team',
        category: 'Data Protection'
    },
    {
        id: 2,
        name: 'AI Model Governance Policy',
        version: 'v1.5',
        status: 'Active',
        lastReview: '2024-11-30',
        nextReview: '2025-05-30',
        owner: 'ML Team',
        category: 'AI Ethics'
    },
    {
        id: 3,
        name: 'Loan Underwriting Standards',
        version: 'v3.2',
        status: 'Under Review',
        lastReview: '2024-12-01',
        nextReview: '2025-03-01',
        owner: 'Risk Management',
        category: 'Credit Risk'
    },
    {
        id: 4,
        name: 'Fraud Prevention Framework',
        version: 'v2.0',
        status: 'Active',
        lastReview: '2024-12-20',
        nextReview: '2025-06-20',
        owner: 'Security Team',
        category: 'Fraud Risk'
    },
    {
        id: 5,
        name: 'Fair Lending Compliance',
        version: 'v1.8',
        status: 'Active',
        lastReview: '2024-12-10',
        nextReview: '2025-03-10',
        owner: 'Legal Team',
        category: 'Regulatory'
    }
]

export default function PoliciesPage() {
    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Governance & Policies</h1>
                <p className="text-muted-foreground">Manage organizational policies and governance frameworks</p>
            </div>

            <div className="grid gap-4 md:grid-cols-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Policies</CardTitle>
                        <FileText className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{policies.length}</div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Active</CardTitle>
                        <CheckCircle className="h-4 w-4 text-green-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {policies.filter(p => p.status === 'Active').length}
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Under Review</CardTitle>
                        <Clock className="h-4 w-4 text-yellow-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {policies.filter(p => p.status === 'Under Review').length}
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Review Due</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-red-500" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">2</div>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Policy Library</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {policies.map((policy) => (
                            <div key={policy.id} className="flex items-center justify-between p-4 border border-border rounded-lg bg-card">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2">
                                        <h3 className="font-semibold text-foreground">{policy.name}</h3>
                                        <Badge variant={policy.status === 'Active' ? 'default' : 'secondary'}>
                                            {policy.status}
                                        </Badge>
                                        <Badge variant="outline">{policy.version}</Badge>
                                    </div>
                                    <div className="text-sm text-muted-foreground mt-1">
                                        <span className="mr-4">Category: {policy.category}</span>
                                        <span className="mr-4">Owner: {policy.owner}</span>
                                        <span>Next Review: {policy.nextReview}</span>
                                    </div>
                                </div>
                                <Button variant="outline" size="sm">View Details</Button>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
