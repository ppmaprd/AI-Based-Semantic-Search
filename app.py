from flask import Flask, request, jsonify, render_template_string
from chatbot import chatbot_response

app = Flask(__name__)

POLICIES = [
    "Risk Assessment Policy","Access Control Policy","Incident Management Policy",
    "Data Classification Policy","Vendor Risk Management Policy","Password Management Policy",
    "Backup and Recovery Policy","Secure Development Policy","Logging and Monitoring Policy",
    "Business Continuity Policy","Network Security Policy","Endpoint Security Policy",
    "Change Management Policy","Asset Management Policy","Encryption Policy",
    "Mobile Device Policy","Physical Security Policy","Email Security Policy"
]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>InfoSec AI Assistant</title>

<style>
body { margin:0; font-family:"Segoe UI"; background:#f1f5f9; }

/* Sidebar */
.sidebar {
    width:260px;
    height:100vh;
    position:fixed;
    background:#0f172a;
    color:white;
    padding:20px;
}
.sidebar h2 { color:#38bdf8; }
.sidebar select {
    width:100%;
    padding:10px;
    margin:10px 0;
    border-radius:6px;
}

/* Main */
.main {
    margin-left:280px;
    padding:20px;
}

/* Chat */
.chat-box {
    background:white;
    height:420px;
    overflow-y:auto;
    padding:15px;
    border-radius:10px;
    box-shadow:0 2px 10px rgba(0,0,0,0.1);
}
.user { text-align:right; color:#2563eb; margin:10px; }

/* Input */
.input-area {
    margin-top:10px;
    display:flex;
}
input {
    flex:1;
    padding:12px;
    border-radius:8px;
    border:1px solid #ccc;
}
button {
    padding:12px;
    margin-left:10px;
    border:none;
    border-radius:8px;
    cursor:pointer;
}
.send-btn { background:#2563eb; color:white; }
.clear-btn { background:#dc2626; color:white; }

/* Suggestions */
#suggestions {
    background:white;
    border:1px solid #ddd;
    border-radius:8px;
    margin-top:5px;
    max-height:200px;
    overflow-y:auto;
}
#suggestions div {
    padding:10px;
    cursor:pointer;
}
#suggestions div:hover {
    background:#f1f5f9;
}
</style>
</head>

<body>

<div class="sidebar">
    <h2>🔐 InfoSec AI</h2>

    <label>Policy</label>
    <select id="policy">
        <option value="">All Policies</option>
        {% for p in policies %}
        <option>{{p}}</option>
        {% endfor %}
    </select>

    <label>Section</label>
    <select id="section">
        <option value="">All Sections</option>
        <option value="purpose">Purpose</option>
        <option value="scope">Scope</option>
        <option value="roles">Roles</option>
        <option value="inputs">Inputs</option>
        <option value="outputs">Outputs</option>
        <option value="compliance">Compliance</option>
        <option value="review">Review</option>
        <option value="records">Records</option>
    </select>
</div>

<div class="main">

<h2>💬 Security Policy Assistant</h2>

<div class="chat-box" id="chat"></div>

<div class="input-area">
<input id="query" placeholder="Ask your question..."
       onkeyup="showSuggestions()" 
       onkeypress="handleKey(event)">
<button class="send-btn" onclick="sendQuery()">Send</button>
<button class="clear-btn" onclick="clearChat()">Clear</button>
</div>

<div id="suggestions"></div>

</div>

<script>

// -------------------------------
// MESSAGE FORMAT
// -------------------------------
function addMessage(text, type){
    let chat = document.getElementById("chat");
    let div = document.createElement("div");

    if(type === "bot"){
        let policy="", section="", answer="", source="";

        text.split("\\n").forEach(line=>{
            if(line.includes("[Policy]")) policy = line.split(":")[1]?.trim();
            if(line.includes("[Section]")) section = line.split(":")[1]?.trim();
            if(line.includes("[Answer]")) answer = line.split(":")[1]?.trim();
            if(line.includes("[Source]")) source = line.split(":")[1]?.trim();
        });

        div.innerHTML = `
        <div style="background:#ecfdf5;padding:15px;border-radius:12px;margin:10px">
            <div style="font-weight:bold;color:#065f46;margin-bottom:8px">
                ✅ Answer
            </div>
            <div style="margin-bottom:12px;font-size:15px;">
                ${answer || text}
            </div>
            <div style="font-size:12px;background:#f1f5f9;padding:8px;border-radius:6px;display:flex;gap:15px;flex-wrap:wrap">
                <span><b>Policy:</b> ${policy || "-"}</span>
                <span><b>Section:</b> ${section || "-"}</span>
                <span><b>Source:</b> ${source || "-"}</span>
            </div>
        </div>`;
    } else {
        div.className = "user";
        div.innerText = text;
    }

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// -------------------------------
function sendQuery(){
    let queryInput = document.getElementById("query");
    let policy = document.getElementById("policy").value;
    let section = document.getElementById("section").value;

    let query = queryInput.value.trim();

    if(!query && !policy){
        addMessage("⚠️ Please select a policy or type a query.", "bot");
        return;
    }

    if(!query){
        query = section ? 
        `What is the ${section} of ${policy}` :
        `Explain ${policy}`;
    }

    let final = query;
    if(policy) final += " in " + policy;
    if(section) final += " for " + section;

    addMessage("You: " + query, "user");

    fetch("/chat", {
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({query:final})
    })
    .then(r=>r.json())
    .then(d=>{
        addMessage(d.answer, "bot");
        document.getElementById("policy").value="";
        document.getElementById("section").value="";
    });

    queryInput.value="";
    document.getElementById("suggestions").innerHTML="";
}

// -------------------------------
function clearChat(){
    document.getElementById("chat").innerHTML="";
}

// -------------------------------
function handleKey(e){
    if(e.key==="Enter") sendQuery();
}

// -------------------------------
// AUTOCOMPLETE
// -------------------------------
const POLICIES = [
"Risk Assessment Policy","Access Control Policy","Incident Management Policy",
"Data Classification Policy","Vendor Risk Management Policy","Password Management Policy",
"Backup and Recovery Policy","Secure Development Policy","Logging and Monitoring Policy",
"Business Continuity Policy","Network Security Policy","Endpoint Security Policy",
"Change Management Policy","Asset Management Policy","Encryption Policy",
"Mobile Device Policy","Physical Security Policy","Email Security Policy"
];

const SECTIONS = [
"purpose","scope","roles and responsibilities","inputs",
"outputs","tools","compliance mapping","review frequency","records"
];

const QUESTION_BANK = [];

POLICIES.forEach(p=>{
    SECTIONS.forEach(s=>{
        QUESTION_BANK.push(`What is the ${s} of ${p}?`);
    });
});

function showSuggestions(){
    let input = document.getElementById("query").value.toLowerCase();
    let box = document.getElementById("suggestions");

    box.innerHTML="";
    if(!input) return;

    QUESTION_BANK
    .filter(q=>q.toLowerCase().includes(input))
    .slice(0,8)
    .forEach(q=>{
        let div=document.createElement("div");
        div.innerHTML = q.replace(new RegExp(input,"gi"), m=>"<b>"+m+"</b>");
        div.onclick=()=>{
            document.getElementById("query").value=q;
            box.innerHTML="";
        };
        box.appendChild(div);
    });
}

// hide suggestions
document.addEventListener("click", function(e){
    if(!e.target.closest("#query")){
        document.getElementById("suggestions").innerHTML="";
    }
});

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_PAGE, policies=POLICIES)

@app.route("/chat", methods=["POST"])
def chat():
    query = request.json.get("query")
    return jsonify({"answer": chatbot_response(query)})

if __name__ == "__main__":
    app.run(debug=True)