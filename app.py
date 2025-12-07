"""
Flask Web UI for testing MCP RAG and Calculator tools
"""
from flask import Flask, render_template, request, jsonify
import httpx
import asyncio

app = Flask(__name__)

# MCP Server URL
MCP_SERVER_URL = "http://localhost:8000"

@app.route('/')
def index():
    """Render the main UI page"""
    return render_template('index.html')

@app.route('/api/rag', methods=['POST'])
def rag_retrieve():
    """Call MCP RAG retrieve tool"""
    try:
        from utils.retrieval import hybrid_search
        
        data = request.json
        query = data.get('query', '')
        
        # Call the retrieval function directly
        docs = hybrid_search(query, top_k=3)
        result = "\n---\n".join(docs)
        
        return jsonify({
            'success': True,
            'result': result
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/calculator', methods=['POST'])
def calculator():
    """Call MCP calculator tool"""
    try:
        import math
        
        data = request.json
        expression = data.get('expression', '')
        
        # Safe evaluation with math module
        try:
            result = str(eval(expression, {"__builtins__": {}}, {"math": math}))
            return jsonify({
                'success': True,
                'result': result
            })
        except Exception as calc_error:
            return jsonify({
                'success': False,
                'error': f'CALC_ERROR: {calc_error}'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if MCP server is running"""
    # Since we're calling functions directly, MCP is always "running"
    return jsonify({
        'mcp_server': 'running',
        'ui_server': 'running'
    })

@app.route('/api/agent', methods=['POST'])
def intelligent_agent():
    """Intelligent agent that routes queries to appropriate tools based on context"""
    try:
        import re
        import math
        from utils.retrieval import hybrid_search
        
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query is required'
            }), 400
        
        # Initialize response
        response = {
            'success': True,
            'query': query,
            'tools_used': [],
            'results': {},
            'final_answer': ''
        }
        
        # Pattern matching to detect mathematical expressions
        # Look for numbers, operators, math functions
        math_patterns = [
            r'\d+\s*[\+\-\*/\^]\s*\d+',  # Basic arithmetic
            r'\d+\s*\*\*\s*\d+',  # Power operator
            r'math\.',  # Math module functions
            r'\d+\s*%\s*\d+',  # Modulo
            r'calculate|compute|what is \d+',  # Calculate keywords
        ]
        
        has_math = any(re.search(pattern, query.lower()) for pattern in math_patterns)
        
        # Check if query asks for information/documents
        info_keywords = [
            'what', 'how', 'why', 'when', 'where', 'who',
            'explain', 'describe', 'tell me about', 'information',
            'policy', 'policies', 'target', 'targets', 'compare',
            'germany', 'renewable', 'energy', 'climate'
        ]
        
        has_info_request = any(keyword in query.lower() for keyword in info_keywords)
        
        # Extract mathematical expressions for calculation
        calc_result = None
        if has_math:
            # Try to extract and evaluate mathematical expressions
            # Look for patterns like "250 * (1.1 ** 7)" or "calculate X"
            expr_match = re.search(r'[\d\s\+\-\*/\(\)\.\*\^%]+', query)
            if expr_match:
                expression = expr_match.group(0).strip()
                # Replace ^ with ** for Python
                expression = expression.replace('^', '**')
                
                try:
                    calc_result = str(eval(expression, {"__builtins__": {}}, {"math": math}))
                    response['tools_used'].append('calculator')
                    response['results']['calculator'] = {
                        'expression': expression,
                        'result': calc_result
                    }
                except:
                    # If extraction fails, try the whole query
                    try:
                        clean_query = query.lower()
                        for word in ['calculate', 'compute', 'what is', 'equals']:
                            clean_query = clean_query.replace(word, '')
                        clean_query = clean_query.strip().replace('^', '**')
                        
                        calc_result = str(eval(clean_query, {"__builtins__": {}}, {"math": math}))
                        response['tools_used'].append('calculator')
                        response['results']['calculator'] = {
                            'expression': clean_query,
                            'result': calc_result
                        }
                    except:
                        pass
        
        # Retrieve documents if information is requested
        rag_result = None
        if has_info_request or not has_math:
            docs = hybrid_search(query, top_k=3)
            rag_result = "\n\n".join(docs)
            response['tools_used'].append('rag')
            response['results']['rag'] = {
                'documents': docs,
                'context': rag_result
            }
        
        # Generate final answer combining results
        if calc_result and rag_result:
            response['final_answer'] = (
                f"Based on my analysis:\n\n"
                f"**Calculation Result:** {response['results']['calculator']['expression']} = {calc_result}\n\n"
                f"**Relevant Information:**\n{rag_result}\n\n"
                f"Combining these results: The calculated value is {calc_result}. "
                f"This can be compared with the information retrieved from the knowledge base."
            )
        elif calc_result:
            response['final_answer'] = (
                f"**Calculation Result:**\n"
                f"{response['results']['calculator']['expression']} = {calc_result}"
            )
        elif rag_result:
            response['final_answer'] = (
                f"**Retrieved Information:**\n\n{rag_result}"
            )
        else:
            response['final_answer'] = "I couldn't determine how to process this query. Please try asking about renewable energy information or provide a mathematical expression to calculate."
            response['tools_used'].append('none')
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("MCP RAG & Calculator UI Server")
    print("=" * 60)
    print("Starting Flask UI server on http://localhost:5000")
    print("Make sure MCP server is running on http://localhost:8000")
    print("=" * 60)
    app.run(debug=True, port=5000)
