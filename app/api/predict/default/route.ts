import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'

export async function POST(request: NextRequest) {
    try {
        const session = await auth()

        if (!session?.user) {
            return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
        }

        const data = await request.json()

        // TODO: Integrate with actual ML model
        // For now, return simulated prediction based on input data

        // Calculate risk factors
        const creditScoreWeight = (850 - data.creditScore) / 550 // Higher score = lower risk
        const dtiWeight = data.dtiRatio // Higher DTI = higher risk
        const incomeToLoanRatio = data.loanAmount / data.income
        const employmentStability = data.monthsEmployed / 120 // Normalize to 10 years

        // Calculate default probability (0-1)
        let defaultProbability =
            (creditScoreWeight * 0.35) +
            (dtiWeight * 0.25) +
            (incomeToLoanRatio * 0.2) +
            ((1 - employmentStability) * 0.1) +
            (data.hasMortgage ? 0.05 : 0) +
            (data.hasCoSigner ? -0.1 : 0.05)

        // Clamp between 0 and 1
        defaultProbability = Math.max(0, Math.min(1, defaultProbability))

        // Calculate risk score (0-1000)
        const riskScore = Math.round(defaultProbability * 1000)

        // Calculate affordability index (0-10)
        const monthlyIncome = data.income / 12
        const monthlyPayment = (data.loanAmount * (data.interestRate / 100 / 12)) /
            (1 - Math.pow(1 + (data.interestRate / 100 / 12), -data.loanTerm))
        const affordabilityIndex = Math.max(0, Math.min(10, (monthlyIncome / monthlyPayment) * 2))

        // Determine key risk factors
        const reasons = []

        if (data.creditScore < 650) {
            reasons.push({
                factor: 'Low credit score',
                impact: 'negative',
                weight: 0.35
            })
        }

        if (data.dtiRatio > 0.4) {
            reasons.push({
                factor: 'High debt-to-income ratio',
                impact: 'negative',
                weight: 0.25
            })
        }

        if (incomeToLoanRatio > 3) {
            reasons.push({
                factor: 'Loan amount high relative to income',
                impact: 'negative',
                weight: 0.2
            })
        }

        if (data.monthsEmployed < 12) {
            reasons.push({
                factor: 'Limited employment history',
                impact: 'negative',
                weight: 0.1
            })
        }

        if (data.hasCoSigner) {
            reasons.push({
                factor: 'Has co-signer',
                impact: 'positive',
                weight: 0.1
            })
        }

        if (data.creditScore >= 750) {
            reasons.push({
                factor: 'Excellent credit score',
                impact: 'positive',
                weight: 0.35
            })
        }

        // Model confidence (simulated)
        const confidence = 0.85 + (Math.random() * 0.1)

        const prediction = {
            defaultProbability,
            riskScore,
            affordabilityIndex,
            confidence,
            reasons,
            decision: defaultProbability > 0.7 ? 'REJECT' :
                defaultProbability > 0.4 ? 'REVIEW' : 'APPROVE',
            modelVersion: 'v1.0.0-ml-pipeline',
            timestamp: new Date().toISOString()
        }

        return NextResponse.json(prediction)

    } catch (error) {
        console.error('Error in loan default prediction:', error)
        return NextResponse.json(
            { error: 'Internal server error' },
            { status: 500 }
        )
    }
}
