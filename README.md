# MCP RAG & Calculator Testing Guide

## 🚀 Quick Start

### 1. Setup Environment (First Time Only)

Run the setup script:
```powershell
.\runme.ps1
```

Or manually:
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the MCP Server

In Terminal 1:
```powershell
# Activate venv if not already activated
.\.venv\Scripts\Activate.ps1

# Start MCP server
python mcp_server.py
```

The MCP server will run on `http://localhost:8000`

### 3. Start the Web UI

In Terminal 2 (new terminal):
```powershell
# Activate venv
.\.venv\Scripts\Activate.ps1

# Start Flask UI
python app.py
```

The UI will be available at `http://localhost:5000`

### 4. Test the Tools

Open your browser and navigate to:
```
http://localhost:5000
```

## 🧪 Testing Examples

### RAG Retrieval Tool
Try these queries:
- "Germany renewable energy policies"
- "Climate change mitigation"
- "Renewable energy targets"

### Calculator Tool
Try these expressions:
- `250 * (1.1 ** 7)` - Calculate growth over 7 years
- `(250 * 1.1**7 - 250) / 250 * 100` - Percentage growth
- `math.sqrt(144)` - Square root
- `math.pi * 10**2` - Circle area

## 📁 Project Structure

```
mcp_rag_cal/
├── mcp_server.py          # MCP server with RAG and calculator tools
├── app.py                 # Flask web UI server
├── templates/
│   └── index.html         # Web UI interface
├── utils/
│   ├── retrieval.py       # RAG retrieval logic
│   └── generation.py      # Answer generation
├── requirements.txt       # Python dependencies
├── runme.ps1             # Windows setup script
└── README.md             # This file
```

## 🔧 Architecture

1. **MCP Server** (`mcp_server.py`):
   - Exposes two tools: `rag_retrieve` and `calculator`
   - Uses FastMCP framework
   - Runs on port 8000

2. **Web UI** (`app.py`):
   - Flask server providing REST API
   - Beautiful modern interface
   - Runs on port 5000

3. **Utils**:
   - `retrieval.py`: Mock document retrieval (replace with real vector DB)
   - `generation.py`: Answer generation utilities

## 🎯 Features

- ✅ RAG document retrieval
- ✅ Safe calculator with math functions
- ✅ Real-time server status monitoring
- ✅ Beautiful, responsive UI
- ✅ Example queries for quick testing
- ✅ Error handling and validation

## 🔄 Troubleshooting

### MCP Server shows "Not Running"
- Make sure you started `mcp_server.py` in a separate terminal
- Check if port 8000 is available
- Look for errors in the MCP server terminal

### Port Already in Use
```powershell
# Find process using port 5000 or 8000
netstat -ano | findstr :5000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Import Errors
Make sure virtual environment is activated and dependencies are installed:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📝 Next Steps

1. **Replace Mock Data**: Update `utils/retrieval.py` with real vector database
2. **Add LLM Integration**: Connect to Ollama or other LLM for answer generation
3. **Add More Tools**: Extend MCP server with additional capabilities
4. **Deploy**: Use production WSGI server like Gunicorn

## 🤝 Contributing

Feel free to enhance the tools, add new features, or improve the UI!
