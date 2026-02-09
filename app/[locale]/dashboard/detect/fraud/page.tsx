'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Shield, AlertTriangle, CheckCircle, XCircle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export default function FraudDetectionPage() {
    const { toast } = useToast()
    const [loading, setLoading] = useState(false)
    const [result, setResult] = useState<any>(null)

    async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault()
        setLoading(true)

        const formData = new FormData(e.currentTarget)
        const data = {
            applicantName: formData.get('name'),
            applicantEmail: formData.get('email'),
            phoneNumber: formData.get('phone'),
            ipAddress: formData.get('ipAddress'),
            deviceId: formData.get('deviceId'),
            income: parseFloat(formData.get('income') as string),
            employmentType: formData.get('employmentType'),
            loanAmount: parseFloat(formData.get('loanAmount') as string),
            creditScore: parseInt(formData.get('creditScore') as string),
            numRecentApplications: parseInt(formData.get('numRecentApplications') as string),
            accountAge: parseInt(formData.get('accountAge') as string),
            hasVerifiedIdentity: formData.get('hasVerifiedIdentity') === 'true',
        }

        try {
            const response = await fetch('/api/detect/fraud', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            })

            const fraudResult = await response.json()
            setResult(fraudResult)

            toast({
                title: fraudResult.isFraud ? 'Fraud Detected!' : 'No Fraud Detected',
                description: `Fraud probability: ${(fraudResult.fraudProbability * 100).toFixed(1)}%`,
                variant: fraudResult.isFraud ? 'destructive' : 'default',
            })
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to detect fraud',
                variant: 'destructive',
            })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Fraud Detection System</h1>
                <p className="text-muted-foreground">Advanced AI-powered fraud detection using behavioral analytics</p>
            </div>

            <div className="grid gap-8 lg:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Application Data</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={onSubmit} className="space-y-4">
                            <div className="space-y-4">
                                <h3 className="font-semibold text-foreground">Personal Information</h3>
                                <div>
                                    <Label htmlFor="name">Applicant Name</Label>
                                    <Input id="name" name="name" required />
                                </div>
                                <div>
                                    <Label htmlFor="email">Email Address</Label>
                                    <Input id="email" name="email" type="email" required />
                                </div>
                                <div>
                                    <Label htmlFor="phone">Phone Number</Label>
                                    <Input id="phone" name="phone" required />
                                </div>
                            </div>

                            <div className="space-y-4 pt-4 border-t border-border">
                                <h3 className="font-semibold text-foreground">Device & Session Data</h3>
                                <div>
                                    <Label htmlFor="ipAddress">IP Address</Label>
                                    <Input id="ipAddress" name="ipAddress" placeholder="192.168.1.1" required />
                                </div>
                                <div>
                                    <Label htmlFor="deviceId">Device ID</Label>
                                    <Input id="deviceId" name="deviceId" required />
                                </div>
                            </div>

                            <div className="space-y-4 pt-4 border-t border-border">
                                <h3 className="font-semibold text-foreground">Financial Information</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="income">Annual Income ($)</Label>
                                        <Input id="income" name="income" type="number" step="0.01" required />
                                    </div>
                                    <div>
                                        <Label htmlFor="loanAmount">Loan Amount ($)</Label>
                                        <Input id="loanAmount" name="loanAmount" type="number" step="0.01" required />
                                    </div>
                                </div>

                                <div>
                                    <Label htmlFor="employmentType">Employment Type</Label>
                                    <Select name="employmentType" required>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select type" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="FULL_TIME">Full-Time</SelectItem>
                                            <SelectItem value="PART_TIME">Part-Time</SelectItem>
                                            <SelectItem value="SELF_EMPLOYED">Self-Employed</SelectItem>
                                            <SelectItem value="UNEMPLOYED">Unemployed</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>

                                <div>
                                    <Label htmlFor="creditScore">Credit Score</Label>
                                    <Input id="creditScore" name="creditScore" type="number" min="300" max="850" required />
                                </div>
                            </div>

                            <div className="space-y-4 pt-4 border-t border-border">
                                <h3 className="font-semibold text-foreground">Behavioral Signals</h3>
                                <div>
                                    <Label htmlFor="numRecentApplications">Recent Applications (Last 30 days)</Label>
                                    <Input id="numRecentApplications" name="numRecentApplications" type="number" min="0" required />
                                </div>
                                <div>
                                    <Label htmlFor="accountAge">Account Age (days)</Label>
                                    <Input id="accountAge" name="accountAge" type="number" min="0" required />
                                </div>
                                <div>
                                    <Label htmlFor="hasVerifiedIdentity">Identity Verified</Label>
                                    <Select name="hasVerifiedIdentity" required>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectItem value="true">Yes</SelectItem>
                                            <SelectItem value="false">No</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                            </div>

                            <Button type="submit" className="w-full" disabled={loading}>
                                {loading ? 'Analyzing...' : 'Detect Fraud'}
                            </Button>
                        </form>
                    </CardContent>
                </Card>

                {result && (
                    <div className="space-y-4">
                        <Card className={result.isFraud ? 'border-red-500 border-2' : 'border-green-500 border-2'}>
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    {result.isFraud ?
                                        <XCircle className="h-6 w-6 text-red-500" /> :
                                        <CheckCircle className="h-6 w-6 text-green-500" />
                                    }
                                    {result.isFraud ? 'FRAUD DETECTED' : 'NO FRAUD DETECTED'}
                                </CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className={`text-center p-8 rounded-lg ${result.isFraud ? 'bg-red-500/10 border border-red-500/20' : 'bg-green-500/10 border border-green-500/20'
                                    }`}>
                                    <Shield className={`h-16 w-16 mx-auto mb-4 ${result.isFraud ? 'text-red-500' : 'text-green-500'
                                        }`} />
                                    <p className="text-sm text-muted-foreground mb-2">Fraud Probability</p>
                                    <p className={`text-5xl font-bold ${result.isFraud ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'
                                        }`}>
                                        {(result.fraudProbability * 100).toFixed(1)}%
                                    </p>
                                </div>

                                <div className="space-y-2">
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Fraud Score:</span>
                                        <Badge variant={result.isFraud ? 'destructive' : 'default'}>
                                            {result.fraudScore}/100
                                        </Badge>
                                    </div>
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Risk Level:</span>
                                        <Badge variant={
                                            result.riskLevel === 'HIGH' ? 'destructive' :
                                                result.riskLevel === 'MEDIUM' ? 'secondary' : 'default'
                                        }>
                                            {result.riskLevel}
                                        </Badge>
                                    </div>
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Recommendation:</span>
                                        <span className="font-bold text-foreground">{result.recommendation}</span>
                                    </div>
                                </div>

                                <Card className="border-l-4 border-l-orange-500">
                                    <CardHeader>
                                        <CardTitle className="text-base flex items-center gap-2">
                                            <AlertTriangle className="h-4 w-4" />
                                            Fraud Indicators Detected
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <ul className="space-y-2">
                                            {result.indicators?.map((indicator: string, i: number) => (
                                                <li key={i} className="flex items-start gap-2">
                                                    <AlertTriangle className="h-4 w-4 text-orange-500 mt-0.5" />
                                                    <span className="text-sm text-foreground">{indicator}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </CardContent>
                                </Card>

                                {result.isFraud && (
                                    <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                                        <p className="text-sm font-semibold text-red-800 dark:text-red-400 mb-2">⚠️ Action Required:</p>
                                        <p className="text-sm text-red-700 dark:text-red-300">
                                            This application requires immediate manual review by the fraud prevention team.
                                            Do not proceed with automated approval.
                                        </p>
                                    </div>
                                )}
                            </CardContent>
                        </Card>
                    </div>
                )}
            </div>
        </div>
    )
}
