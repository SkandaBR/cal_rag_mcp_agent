# MCP RAG & Calculator - Call Hierarchy & Flow

## 🎯 System Overview

This application demonstrates an **intelligent agent** that uses the **Model Context Protocol (MCP)** to automatically select and invoke tools based on user queries. Think of it as a smart assistant that knows when to search for information and when to do calculations.

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                    (Web Browser)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP Request
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK WEB SERVER                          │
│                      (app.py)                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  /api/agent endpoint                                 │   │
│  │  - Pattern matching for tool selection               │   │
│  │  - Query analysis                                    │   │
│  │  - Response formatting                               │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────┬────────────────────────┬────────────────────────┘
             │                        │
             │ Direct Function Call   │ Direct Function Call
             ▼                        ▼
    ┌────────────────┐      ┌─────────────────────┐
    │  RAG RETRIEVAL │      │    CALCULATOR       │
    │ (utils/        │      │  (math evaluation)  │
    │  retrieval.py) │      │                     │
    └────────────────┘      └─────────────────────┘
             │
             │ Returns documents
             ▼
    ┌────────────────┐
    │  MOCK VECTOR   │
    │   DATABASE     │
    │ (in-memory)    │
    └────────────────┘
```

---

## 🔄 Detailed Call Flow

### **Scenario 1: User Asks an Information Query**

**Example**: "What are Germany's renewable energy targets?"

```
1. USER types query in browser
   └─> index.html (textarea#query-input)

2. JavaScript captures input
   └─> Event listener on "Send" button click
   
3. AJAX POST request sent
   └─> fetch('/api/agent', { query: "What are..." })
   
4. Flask receives request
   └─> app.py @app.route('/api/agent', methods=['POST'])
   
5. Query Analysis (Pattern Matching)
   ├─> Check for math patterns: ❌ No math detected
   └─> Check for info keywords: ✅ "what", "targets" found
   
6. Tool Selection Decision
   └─> has_info_request = True
       has_math = False
       → Use RAG ONLY
   
7. Call RAG Retrieval
   └─> from utils.retrieval import hybrid_search
       └─> hybrid_search(query, top_k=3)
           └─> Mock keyword matching
               └─> Returns 3 relevant documents
   
8. Format Response
   └─> response = {
         'tools_used': ['rag'],
         'final_answer': "Retrieved Information:\n\n[docs]"
       }
   
9. Send JSON response to browser
   └─> return jsonify(response)
   
10. JavaScript receives response
    └─> addMessage('agent', data.final_answer, data.tools_used)
        └─> Creates message bubble with 📚 RAG badge
        
11. USER sees answer with tool badge
```

---

### **Scenario 2: User Asks a Calculation Query**

**Example**: "Calculate 250 * (1.1 ** 7)"

```
1. USER types query in browser
   └─> index.html (textarea#query-input)

2. JavaScript captures input
   └─> Event listener on "Send" button click
   
3. AJAX POST request sent
   └─> fetch('/api/agent', { query: "Calculate..." })
   
4. Flask receives request
   └─> app.py @app.route('/api/agent', methods=['POST'])
   
5. Query Analysis (Pattern Matching)
   ├─> Check for math patterns: ✅ "250 * (1.1 ** 7)" detected
   └─> Check for info keywords: ❌ No info keywords
   
6. Tool Selection Decision
   └─> has_math = True
       has_info_request = False
       → Use CALCULATOR ONLY
   
7. Extract Mathematical Expression
   └─> Regex: r'[\d\s\+\-\*/\(\)\.\*\^%]+'
       └─> Extracted: "250 * (1.1 ** 7)"
       
8. Safe Evaluation
   └─> eval(expression, {"__builtins__": {}}, {"math": math})
       └─> Result: 487.1792750000003
   
9. Format Response
   └─> response = {
         'tools_used': ['calculator'],
         'results': {
           'calculator': {
             'expression': '250 * (1.1 ** 7)',
             'result': '487.1792750000003'
           }
         },
         'final_answer': "Calculation Result:\n250 * (1.1 ** 7) = 487.18..."
       }
   
10. Send JSON response to browser
    └─> return jsonify(response)
   
11. JavaScript receives response
    └─> addMessage('agent', data.final_answer, data.tools_used)
        └─> Creates message bubble with 🔢 Calculator badge
        
12. USER sees calculation result with tool badge
```

---

### **Scenario 3: User Asks a Combined Query**

**Example**: "If Germany had 250 TWh in 2023 growing 10% yearly, what will it be in 2030? Compare to targets."

```
1. USER types query in browser
   └─> index.html (textarea#query-input)

2. JavaScript captures input
   └─> Event listener on "Send" button click
   
3. AJAX POST request sent
   └─> fetch('/api/agent', { query: "If Germany..." })
   
4. Flask receives request
   └─> app.py @app.route('/api/agent', methods=['POST'])
   
5. Query Analysis (Pattern Matching)
   ├─> Check for math patterns: ✅ "250", "10%", "2030" detected
   └─> Check for info keywords: ✅ "what", "compare", "targets", "Germany" found
   
6. Tool Selection Decision
   └─> has_math = True
       has_info_request = True
       → Use BOTH TOOLS
   
7. PARALLEL EXECUTION:
   
   ┌─────────────────────────┐    ┌──────────────────────────┐
   │  Calculator Path        │    │  RAG Retrieval Path      │
   ├─────────────────────────┤    ├──────────────────────────┤
   │ Extract: "250 * 1.1**7" │    │ hybrid_search(query, 3)  │
   │ Evaluate expression     │    │ Returns 3 documents      │
   │ Result: 487.18...       │    │ About Germany targets    │
   └─────────────────────────┘    └──────────────────────────┘
             │                              │
             └──────────┬───────────────────┘
                        ▼
8. Combine Results
   └─> response = {
         'tools_used': ['calculator', 'rag'],
         'results': {
           'calculator': { ... },
           'rag': { ... }
         },
         'final_answer': "Based on my analysis:\n\n
                          **Calculation Result:** 250 * (1.1 ** 7) = 487.18\n\n
                          **Relevant Information:**\n[documents]\n\n
                          Combining these results: The calculated value is 487.18.
                          This can be compared with the information retrieved..."
       }
   
9. Send JSON response to browser
    └─> return jsonify(response)
   
10. JavaScript receives response
    └─> addMessage('agent', data.final_answer, data.tools_used)
        └─> Creates message bubble with BOTH badges:
            🔢 Calculator + 📚 RAG Retrieval
        
11. USER sees combined answer with both tool badges
```

---

## 🗂️ File-by-File Breakdown

### **1. index.html** (Frontend)
**Role**: User Interface

```
User Input → JavaScript Event Handlers → AJAX Calls → Display Results
```

**Key Components**:
- `<textarea id="query-input">` - Single input for all queries
- `<div id="chat-messages">` - Conversation history
- `sendQuery()` function - Sends POST to `/api/agent`
- `addMessage()` function - Displays responses with tool badges

---

### **2. app.py** (Backend - Flask Server)
**Role**: Request Router & Intelligent Agent

```
HTTP Request → Pattern Analysis → Tool Selection → Response Formatting
```

**Key Functions**:

#### `@app.route('/api/agent')`
The brain of the system!

```python
1. Receive query from frontend
2. Analyze query with regex patterns:
   - Math patterns: \d+\s*[\+\-\*/\^]\s*\d+
   - Info keywords: what, how, Germany, renewable, etc.
3. Decide which tools to use:
   - has_math → Calculator
   - has_info_request → RAG
   - Both → Both tools
4. Execute selected tools
5. Format combined response
6. Return JSON to frontend
```

**Other Endpoints**:
- `/api/health` - Health check
- `/api/rag` - Direct RAG call (legacy)
- `/api/calculator` - Direct calculator call (legacy)

---

### **3. utils/retrieval.py** (RAG Component)
**Role**: Document Retrieval

```
Query → Keyword Matching → Return Top-K Documents
```

**Key Function**: `hybrid_search(query, top_k=3)`

```python
1. Receive search query
2. Match keywords against mock document database
3. Return top 3 most relevant documents
```

**Current Implementation**: Mock in-memory database
**Production**: Would connect to vector database (ChromaDB, Pinecone, etc.)

---

### **4. utils/generation.py** (Answer Generation)
**Role**: Response Generation (Placeholder)

Currently just a placeholder. In production, this would:
- Take query + retrieved context
- Call LLM (GPT, Claude, Ollama)
- Generate natural language answer

---

### **5. mcp_server.py** (MCP Server - Optional)
**Role**: Standalone MCP Server

This file demonstrates how to create a proper MCP server using FastMCP. Currently **not used** by the web UI (we call functions directly), but shows the MCP pattern:

```python
@mcp.tool()
def rag_retrieve(query: str) -> str:
    """Tool exposed via MCP protocol"""
    
@mcp.tool()
def calculator(expression: str) -> str:
    """Tool exposed via MCP protocol"""
```

---

### **6. agent_mcp.py** (LangChain Agent - Reference)
**Role**: Example of LangChain Integration

Shows how to integrate with LangChain agents and Ollama LLM. Not currently used by the web UI, but demonstrates the pattern for future enhancement.

---

## 🧠 Decision Logic (Pattern Matching)

### **Math Detection Patterns**:
```python
math_patterns = [
    r'\d+\s*[\+\-\*/\^]\s*\d+',    # 250 * 7
    r'\d+\s*\*\*\s*\d+',            # 2 ** 8
    r'math\.',                       # math.sqrt()
    r'\d+\s*%\s*\d+',               # 10 % 3
    r'calculate|compute|what is \d+' # Keywords
]
```

### **Information Keywords**:
```python
info_keywords = [
    'what', 'how', 'why', 'when', 'where', 'who',
    'explain', 'describe', 'tell me about',
    'policy', 'targets', 'compare',
    'germany', 'renewable', 'energy', 'climate'
]
```

### **Decision Tree**:
```
Query Received
    │
    ├─> Contains math patterns?
    │   ├─> YES: has_math = True
    │   └─> NO: has_math = False
    │
    ├─> Contains info keywords?
    │   ├─> YES: has_info_request = True
    │   └─> NO: has_info_request = False
    │
    └─> Tool Selection:
        ├─> has_math AND has_info_request → Use BOTH
        ├─> has_math ONLY → Use Calculator
        ├─> has_info_request ONLY → Use RAG
        └─> Neither → Return error message
```

---

## 🔐 Security Features

### **Safe Expression Evaluation**:
```python
eval(expression, {"__builtins__": {}}, {"math": math})
```

- `{"__builtins__": {}}` - Disables all built-in functions (no `open()`, `exec()`, etc.)
- `{"math": math}` - Only allows `math` module functions
- Prevents code injection attacks

---

## 📡 Data Flow Summary

```
┌──────────┐
│  Browser │
└────┬─────┘
     │ 1. User types query
     │ 2. Click Send
     ▼
┌──────────────┐
│  JavaScript  │
└────┬─────────┘
     │ 3. POST /api/agent
     ▼
┌──────────────┐
│  Flask App   │
│  (app.py)    │
└────┬─────────┘
     │ 4. Pattern matching
     │ 5. Tool selection
     ├─────────┬──────────┐
     ▼         ▼          ▼
┌─────────┐ ┌────────┐ ┌──────┐
│   RAG   │ │  Calc  │ │ Both │
└─────────┘ └────────┘ └──────┘
     │         │          │
     └─────────┴──────────┘
               │ 6. Combine results
               ▼
          ┌──────────┐
          │   JSON   │
          │ Response │
          └────┬─────┘
               │ 7. Return to browser
               ▼
          ┌──────────┐
          │ Display  │
          │ with     │
          │ badges   │
          └──────────┘
```

---

## 🚀 Quick Reference

### **To Start the Application**:
```powershell
# Terminal 1: Start MCP server (optional)
.\.venv\Scripts\python.exe mcp_server.py

# Terminal 2: Start Flask UI
.\.venv\Scripts\python.exe app.py

# Open browser
http://localhost:5000
```

### **Key URLs**:
- Main UI: `http://localhost:5000`
- Health Check: `http://localhost:5000/api/health`
- Agent Endpoint: `POST http://localhost:5000/api/agent`

---

## 💡 For Novice Developers

**Think of it like this**:

1. **Frontend (HTML/JS)** = The restaurant menu and waiter
   - Takes your order (query)
   - Brings back your food (response)

2. **Backend (Flask)** = The kitchen manager
   - Reads your order
   - Decides which chef to call (tool selection)
   - Combines the dishes (response formatting)

3. **RAG Tool** = The recipe book chef
   - Looks up information in the cookbook
   - Returns relevant recipes (documents)

4. **Calculator Tool** = The math chef
   - Does all the calculations
   - Returns precise numbers

5. **Pattern Matching** = The smart order reader
   - Reads "I want pizza" → Calls pizza chef
   - Reads "How much is 2+2?" → Calls math chef
   - Reads "Pizza for 10 people, how many slices?" → Calls BOTH chefs!

The magic is in the **automatic decision-making** - you don't tell the system which tool to use, it figures it out from your question! 🎯
