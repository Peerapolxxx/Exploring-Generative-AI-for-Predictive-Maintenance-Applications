DOCUMENT_CONTEXT_PROMPT = """
<document>
{doc_content}
</document>
"""

CHUNK_CONTEXT_PROMPT = """
Given the following chunk from a machine health report:
<chunk>
{chunk_content}
</chunk>

You are an AI assistant specialized in industrial equipment analysis. Analyze this text segment focusing on:

1. Component Status: Identify the specific machine components or systems being discussed
2. Performance Metrics: Extract and interpret key performance indicators, measurements, or test results
3. Health Indicators: Highlight any anomalies, warnings, or notable patterns in the data
4. Operational Impact: Assess how these findings affect the overall system functionality
5. Maintenance Implications: Note any maintenance requirements or recommendations suggested by the data

Provide a concise, technical summary (2-3 sentences) that:
- Emphasizes the most critical findings
- Uses precise technical terminology
- Connects this chunk's information to overall system health
- Highlights actionable insights for maintenance teams

Focus solely on information present in the chunk. Be specific and quantitative where possible.
Respond only with the technical summary, without any additional commentary or explanations.
"""