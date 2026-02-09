'use client'

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Progress } from '@/components/ui/progress'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

export default function LoanDefaultPredictionPage() {
    const { toast } = useToast()
    const [loading, setLoading] = useState(false)
    const [prediction, setPrediction] = useState<any>(null)

    async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault()
        setLoading(true)

        const formData = new FormData(e.currentTarget)
        const data = {
            age: parseInt(formData.get('age') as string),
            income: parseFloat(formData.get('income') as string),
            education: formData.get('education'),
            employmentType: formData.get('employmentType'),
            maritalStatus: formData.get('maritalStatus'),
            monthsEmployed: parseInt(formData.get('monthsEmployed') as string),
            loanAmount: parseFloat(formData.get('loanAmount') as string),
            loanTerm: parseInt(formData.get('loanTerm') as string),
            interestRate: parseFloat(formData.get('interestRate') as string),
            loanPurpose: formData.get('loanPurpose'),
            creditScore: parseInt(formData.get('creditScore') as string),
            dtiRatio: parseFloat(formData.get('dtiRatio') as string),
            numCreditLines: parseInt(formData.get('numCreditLines') as string),
            hasMortgage: formData.get('hasMortgage') === 'true',
            hasDependents: formData.get('hasDependents') === 'true',
            hasCoSigner: formData.get('hasCoSigner') === 'true',
        }

        try {
            const response = await fetch('/api/predict/default', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            })

            const result = await response.json()
            setPrediction(result)

            toast({
                title: 'Prediction Complete',
                description: `Default probability: ${(result.defaultProbability * 100).toFixed(1)}%`,
            })
        } catch (error) {
            toast({
                title: 'Error',
                description: 'Failed to predict default',
                variant: 'destructive',
            })
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-3xl font-bold text-foreground">Loan Default Prediction</h1>
                <p className="text-muted-foreground">Predict probability of loan default using advanced ML models</p>
            </div>

            <div className="grid gap-8 lg:grid-cols-2">
                <Card>
                    <CardHeader>
                        <CardTitle>Applicant & Loan Information</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={onSubmit} className="space-y-4">
                            {/* Applicant Info */}
                            <div className="space-y-4">
                                <h3 className="font-semibold text-foreground">Applicant Information</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="age">Age</Label>
                                        <Input id="age" name="age" type="number" min="18" max="100" required />
                                    </div>
                                    <div>
                                        <Label htmlFor="income">Annual Income ($)</Label>
                                        <Input id="income" name="income" type="number" step="0.01" required />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="education">Education</Label>
                                        <Select name="education" required>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select education" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="HIGH_SCHOOL">High School</SelectItem>
                                                <SelectItem value="BACHELOR">Bachelor's Degree</SelectItem>
                                                <SelectItem value="MASTER">Master's Degree</SelectItem>
                                                <SelectItem value="PHD">PhD</SelectItem>
                                            </SelectContent>
                                        </Select>
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
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="maritalStatus">Marital Status</Label>
                                        <Select name="maritalStatus" required>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select status" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="SINGLE">Single</SelectItem>
                                                <SelectItem value="MARRIED">Married</SelectItem>
                                                <SelectItem value="DIVORCED">Divorced</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div>
                                        <Label htmlFor="monthsEmployed">Months Employed</Label>
                                        <Input id="monthsEmployed" name="monthsEmployed" type="number" min="0" required />
                                    </div>
                                </div>
                            </div>

                            {/* Loan Details */}
                            <div className="space-y-4 pt-4 border-t border-border">
                                <h3 className="font-semibold text-foreground">Loan Details</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="loanAmount">Loan Amount ($)</Label>
                                        <Input id="loanAmount" name="loanAmount" type="number" step="0.01" required />
                                    </div>
                                    <div>
                                        <Label htmlFor="loanTerm">Loan Term (months)</Label>
                                        <Input id="loanTerm" name="loanTerm" type="number" min="12" max="360" required />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="interestRate">Interest Rate (%)</Label>
                                        <Input id="interestRate" name="interestRate" type="number" step="0.01" min="0" max="50" required />
                                    </div>
                                    <div>
                                        <Label htmlFor="loanPurpose">Loan Purpose</Label>
                                        <Select name="loanPurpose" required>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select purpose" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="DEBT_CONSOLIDATION">Debt Consolidation</SelectItem>
                                                <SelectItem value="HOME_IMPROVEMENT">Home Improvement</SelectItem>
                                                <SelectItem value="BUSINESS">Business</SelectItem>
                                                <SelectItem value="AUTO">Auto</SelectItem>
                                                <SelectItem value="EDUCATION">Education</SelectItem>
                                                <SelectItem value="OTHER">Other</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                            </div>

                            {/* Risk Factors */}
                            <div className="space-y-4 pt-4 border-t border-border">
                                <h3 className="font-semibold text-foreground">Risk Factors</h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <Label htmlFor="creditScore">Credit Score</Label>
                                        <Input id="creditScore" name="creditScore" type="number" min="300" max="850" required />
                                    </div>
                                    <div>
                                        <Label htmlFor="dtiRatio">Debt-to-Income Ratio</Label>
                                        <Input id="dtiRatio" name="dtiRatio" type="number" step="0.01" min="0" max="1" required />
                                    </div>
                                </div>

                                <div>
                                    <Label htmlFor="numCreditLines">Number of Credit Lines</Label>
                                    <Input id="numCreditLines" name="numCreditLines" type="number" min="0" required />
                                </div>

                                <div className="grid grid-cols-3 gap-4">
                                    <div>
                                        <Label htmlFor="hasMortgage">Has Mortgage</Label>
                                        <Select name="hasMortgage" required>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="true">Yes</SelectItem>
                                                <SelectItem value="false">No</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div>
                                        <Label htmlFor="hasDependents">Has Dependents</Label>
                                        <Select name="hasDependents" required>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                <SelectItem value="true">Yes</SelectItem>
                                                <SelectItem value="false">No</SelectItem>
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div>
                                        <Label htmlFor="hasCoSigner">Has Co-Signer</Label>
                                        <Select name="hasCoSigner" required>
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
                            </div>

                            <Button type="submit" className="w-full" disabled={loading}>
                                {loading ? 'Analyzing...' : 'Predict Default Risk'}
                            </Button>
                        </form>
                    </CardContent>
                </Card>

                {prediction && (
                    <div className="space-y-4">
                        <Card>
                            <CardHeader>
                                <CardTitle>Default Prediction Results</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-6">
                                <div className="text-center p-6 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-lg border border-blue-500/20">
                                    <p className="text-sm text-muted-foreground mb-2">Default Probability</p>
                                    <p className="text-5xl font-bold text-indigo-600 dark:text-indigo-400">
                                        {(prediction.defaultProbability * 100).toFixed(1)}%
                                    </p>
                                </div>

                                <div>
                                    <div className="flex justify-between mb-2">
                                        <span className="text-sm font-medium text-foreground">Risk Level</span>
                                        <span className="text-sm font-medium text-foreground">
                                            {prediction.defaultProbability > 0.7 ? 'High' :
                                                prediction.defaultProbability > 0.4 ? 'Medium' : 'Low'}
                                        </span>
                                    </div>
                                    <Progress
                                        value={prediction.defaultProbability * 100}
                                        className="h-3"
                                    />
                                </div>

                                <div className="space-y-2">
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Risk Score:</span>
                                        <span className="font-bold text-foreground">{prediction.riskScore?.toFixed(0)}/1000</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Affordability Index:</span>
                                        <span className="font-bold text-foreground">{prediction.affordabilityIndex?.toFixed(1)}/10</span>
                                    </div>
                                    <div className="flex justify-between p-3 bg-muted rounded">
                                        <span className="text-foreground">Confidence:</span>
                                        <span className="font-bold text-foreground">{(prediction.confidence * 100).toFixed(1)}%</span>
                                    </div>
                                </div>

                                <Card className="border-l-4 border-l-indigo-500">
                                    <CardHeader>
                                        <CardTitle className="text-base">Key Risk Factors</CardTitle>
                                    </CardHeader>
                                    <CardContent>
                                        <ul className="space-y-2">
                                            {prediction.reasons?.map((reason: any, i: number) => (
                                                <li key={i} className="flex items-start gap-2">
                                                    {reason.impact === 'negative' ?
                                                        <TrendingDown className="h-4 w-4 text-red-500 mt-0.5" /> :
                                                        <TrendingUp className="h-4 w-4 text-green-500 mt-0.5" />
                                                    }
                                                    <span className="text-sm text-foreground">{reason.factor} ({(reason.weight * 100).toFixed(0)}% weight)</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </CardContent>
                                </Card>
                            </CardContent>
                        </Card>
                    </div>
                )}
            </div>
        </div>
    )
}
