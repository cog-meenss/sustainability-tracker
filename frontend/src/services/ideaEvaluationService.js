import { getChatResponse } from './openaiService';

// Default evaluation parameters
const DEFAULT_EVALUATION_PARAMETERS = {
  feasibility: {
    weight: 0.25,
    description: 'Technical and practical viability of implementation'
  },
  impact: {
    weight: 0.30,
    description: 'Potential business impact and value creation'
  },
  innovation: {
    weight: 0.20,
    description: 'Novelty and competitive advantage'
  },
  cost: {
    weight: 0.15,
    description: 'Implementation cost and resource requirements'
  },
  timeline: {
    weight: 0.10,
    description: 'Speed of implementation and time to market'
  }
};

// Generate evaluation prompt for OpenAI
const generateEvaluationPrompt = (idea, parameters) => {
  const parameterDescriptions = Object.entries(parameters)
    .map(([key, param]) => `- ${key.charAt(0).toUpperCase() + key.slice(1)} (${(param.weight * 100).toFixed(0)}%): ${param.description}`)
    .join('\n');

  return `You are an expert business analyst evaluating business ideas. Please evaluate the following idea across multiple criteria and provide detailed feedback.

**Idea to Evaluate:**
${JSON.stringify(idea, null, 2)}

**Evaluation Criteria:**
${parameterDescriptions}

**Instructions:**
1. Score each criterion from 1-10 (10 being excellent, 1 being poor)
2. Provide specific reasoning for each score
3. Calculate an overall weighted score
4. Give actionable recommendations for improvement
5. Identify potential risks and mitigation strategies

**Response Format (JSON):**
{
  "scores": {
    "feasibility": { "score": X, "reasoning": "..." },
    "impact": { "score": X, "reasoning": "..." },
    "innovation": { "score": X, "reasoning": "..." },
    "cost": { "score": X, "reasoning": "..." },
    "timeline": { "score": X, "reasoning": "..." }
  },
  "overallScore": X.XX,
  "overallRanking": "Excellent/Good/Average/Poor",
  "summary": "Brief overall assessment...",
  "recommendations": ["Recommendation 1", "Recommendation 2", "..."],
  "risks": ["Risk 1", "Risk 2", "..."],
  "mitigations": ["Mitigation 1", "Mitigation 2", "..."],
  "implementationPriority": "High/Medium/Low",
  "estimatedEffort": "Low/Medium/High",
  "marketReadiness": "Ready/6-12 months/1-2 years/Long-term"
}

Ensure all scores are realistic and well-justified. Be constructive but honest in your evaluation.`;
};

// Fallback evaluation for when OpenAI is not available
const generateFallbackEvaluation = (idea, parameters) => {
  // Simple keyword-based scoring
  const ideaText = JSON.stringify(idea).toLowerCase();
  
  const keywordScores = {
    feasibility: calculateKeywordScore(ideaText, [
      'simple', 'easy', 'existing', 'standard', 'proven', 'available', 'ready',
      'complex', 'difficult', 'new', 'experimental', 'research', 'prototype'
    ]),
    impact: calculateKeywordScore(ideaText, [
      'revenue', 'profit', 'customer', 'market', 'growth', 'efficiency', 'save',
      'cost', 'expense', 'minor', 'small', 'limited', 'niche'
    ]),
    innovation: calculateKeywordScore(ideaText, [
      'new', 'novel', 'innovative', 'unique', 'breakthrough', 'disruptive',
      'existing', 'standard', 'common', 'traditional', 'conventional'
    ]),
    cost: calculateKeywordScore(ideaText, [
      'low', 'cheap', 'affordable', 'budget', 'minimal', 'cost-effective',
      'expensive', 'costly', 'high', 'investment', 'capital', 'resources'
    ], true), // Invert for cost (lower cost = higher score)
    timeline: calculateKeywordScore(ideaText, [
      'quick', 'fast', 'immediate', 'short', 'rapid', 'soon',
      'long', 'slow', 'extended', 'months', 'years', 'delayed'
    ])
  };

  // Calculate weighted overall score
  const overallScore = Object.entries(parameters).reduce((total, [key, param]) => {
    return total + (keywordScores[key] * param.weight);
  }, 0);

  const ranking = overallScore >= 8 ? 'Excellent' : 
                 overallScore >= 6.5 ? 'Good' : 
                 overallScore >= 5 ? 'Average' : 'Poor';

  return {
    scores: Object.fromEntries(
      Object.keys(parameters).map(key => [
        key, 
        { 
          score: keywordScores[key], 
          reasoning: `Automated assessment based on content analysis. ${keywordScores[key] >= 7 ? 'Positive indicators found.' : keywordScores[key] >= 5 ? 'Mixed indicators.' : 'Challenging aspects identified.'}` 
        }
      ])
    ),
    overallScore: Math.round(overallScore * 100) / 100,
    overallRanking: ranking,
    summary: `Automated evaluation suggests this idea has ${ranking.toLowerCase()} potential based on content analysis.`,
    recommendations: [
      'Consider detailed market research',
      'Develop a proof of concept',
      'Assess resource requirements',
      'Identify key stakeholders'
    ],
    risks: [
      'Market acceptance uncertainty',
      'Technical implementation challenges',
      'Resource availability',
      'Competitive response'
    ],
    mitigations: [
      'Conduct pilot testing',
      'Phased implementation approach',
      'Stakeholder engagement',
      'Risk monitoring framework'
    ],
    implementationPriority: overallScore >= 7 ? 'High' : overallScore >= 5.5 ? 'Medium' : 'Low',
    estimatedEffort: overallScore <= 6 ? 'High' : overallScore <= 8 ? 'Medium' : 'Low',
    marketReadiness: overallScore >= 7.5 ? 'Ready' : overallScore >= 6 ? '6-12 months' : overallScore >= 4 ? '1-2 years' : 'Long-term',
    isAutomated: true
  };
};

// Helper function for keyword-based scoring
const calculateKeywordScore = (text, keywords, invert = false) => {
  const positiveKeywords = keywords.slice(0, Math.floor(keywords.length / 2));
  const negativeKeywords = keywords.slice(Math.floor(keywords.length / 2));
  
  let score = 5; // Base score
  
  positiveKeywords.forEach(keyword => {
    if (text.includes(keyword)) score += 0.5;
  });
  
  negativeKeywords.forEach(keyword => {
    if (text.includes(keyword)) score -= 0.5;
  });
  
  score = Math.max(1, Math.min(10, score)); // Clamp between 1-10
  
  return invert ? (11 - score) : score;
};

// Main evaluation function
export const evaluateIdea = async (idea, customParameters = null) => {
  const parameters = customParameters || DEFAULT_EVALUATION_PARAMETERS;
  
  try {
    const prompt = generateEvaluationPrompt(idea, parameters);
    
    // Try OpenAI first
    const result = await getChatResponse([
      { role: 'user', content: prompt }
    ]);

    if (result.success) {
      try {
        // Try to parse JSON response
        const evaluation = JSON.parse(result.response);
        
        // Validate the response structure
        if (evaluation.scores && evaluation.overallScore !== undefined) {
          return {
            success: true,
            evaluation: {
              ...evaluation,
              isAutomated: false,
              evaluationDate: new Date().toISOString()
            }
          };
        }
      } catch (parseError) {
        console.warn('Failed to parse OpenAI response as JSON, using fallback');
      }
    }
    
    // Fallback to automated evaluation
    console.info('Using fallback evaluation method');
    return {
      success: true,
      evaluation: {
        ...generateFallbackEvaluation(idea, parameters),
        evaluationDate: new Date().toISOString()
      },
      usedFallback: true
    };
    
  } catch (error) {
    console.error('Error during idea evaluation:', error);
    
    // Return fallback evaluation on error
    return {
      success: true,
      evaluation: {
        ...generateFallbackEvaluation(idea, parameters),
        evaluationDate: new Date().toISOString(),
        error: 'AI evaluation failed, using automated assessment'
      },
      usedFallback: true,
      error: error.message
    };
  }
};

// Batch evaluate multiple ideas
export const evaluateIdeas = async (ideas, customParameters = null, onProgress = null) => {
  const results = [];
  const totalIdeas = ideas.length;
  
  for (let i = 0; i < totalIdeas; i++) {
    const idea = ideas[i];
    
    // Add a small delay between evaluations to respect rate limits
    if (i > 0) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    const result = await evaluateIdea(idea, customParameters);
    results.push({
      ideaIndex: i,
      ideaId: idea.id || i,
      ...result
    });
    
    // Report progress
    if (onProgress) {
      onProgress({
        completed: i + 1,
        total: totalIdeas,
        percentage: Math.round(((i + 1) / totalIdeas) * 100)
      });
    }
  }
  
  // Sort by overall score (highest first)
  results.sort((a, b) => (b.evaluation?.overallScore || 0) - (a.evaluation?.overallScore || 0));
  
  return results;
};

// Get evaluation parameters with defaults
export const getEvaluationParameters = () => {
  return { ...DEFAULT_EVALUATION_PARAMETERS };
};

// Validate custom parameters
export const validateParameters = (parameters) => {
  if (!parameters || typeof parameters !== 'object') {
    return { valid: false, error: 'Parameters must be an object' };
  }
  
  const totalWeight = Object.values(parameters).reduce((sum, param) => {
    return sum + (param.weight || 0);
  }, 0);
  
  if (Math.abs(totalWeight - 1.0) > 0.01) {
    return { valid: false, error: 'Parameter weights must sum to 1.0' };
  }
  
  return { valid: true };
};

// Format evaluation for display
export const formatEvaluationSummary = (evaluation) => {
  if (!evaluation) return 'No evaluation available';
  
  const { overallScore, overallRanking, implementationPriority, isAutomated } = evaluation;
  const source = isAutomated ? '(Automated)' : '(AI-Powered)';
  
  return `Score: ${overallScore?.toFixed(1)}/10 | Ranking: ${overallRanking} | Priority: ${implementationPriority} ${source}`;
};