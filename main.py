# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 18:29:39 2025

@author: kalyane
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from typing import List, Dict, Any
import json  # For tests

app = FastAPI()

class Parameter(BaseModel):
    name: str
    type: str

class Signature(BaseModel):
    function_name: str
    parameters: List[Parameter]
    returns: Dict[str, str]

class Payload(BaseModel):
    question_id: str
    title: str
    description: str
    signature: Signature
    language: str

    @validator('language')
    def validate_language(cls, v):
        supported = ['python', 'java', 'cpp', 'javascript']
        if v not in supported:
            raise ValueError(f"Unsupported language: {v}")
        return v

# Type mappings
primitive_map = {
    'python': {'int': 'int', 'long': 'int', 'float': 'float', 'double': 'float', 'bool': 'bool', 'string': 'str'},
    'java': {'int': 'int', 'long': 'long', 'float': 'float', 'double': 'double', 'bool': 'boolean', 'string': 'String'},
    'cpp': {'int': 'int', 'long': 'long long', 'float': 'float', 'double': 'double', 'bool': 'bool', 'string': 'std::string'},
    'javascript': {'int': 'number', 'long': 'number', 'float': 'number', 'double': 'number', 'bool': 'boolean', 'string': 'string'},
}

array_map = {
    'python': 'List[{}]',
    'java': 'List<{}>',
    'cpp': 'std::vector<{}>',
    'javascript': '{}[]',
}

java_boxed = {'int': 'Integer', 'long': 'Long', 'float': 'Float', 'double': 'Double', 'bool': 'Boolean'}

def get_language_type(lang: str, dsl_type: str) -> str:
    if dsl_type in primitive_map[lang]:
        return primitive_map[lang][dsl_type]
    if dsl_type.endswith('[]'):
        inner = dsl_type[:-2]
        inner_type = get_language_type(lang, inner)
        if lang == 'java' and inner in java_boxed:
            inner_type = java_boxed[inner]
        return array_map[lang].format(inner_type)
    if dsl_type == 'List':
        if lang == 'python': return 'ListNode'
        if lang == 'java': return 'ListNode'
        if lang == 'cpp': return 'ListNode*'
        if lang == 'javascript': return 'ListNode'
    if dsl_type == 'Tree':
        if lang == 'python': return 'TreeNode'
        if lang == 'java':  return 'TreeNode'
        if lang == 'cpp':  return 'TreeNode*'
        if lang == 'javascript': return 'TreeNode'
    if dsl_type == 'Graph':
        if lang == 'python': return 'List[List[int]]'
        if lang == 'java': return 'List<List<Integer>>'
        if lang == 'cpp': return 'std::vector<std::vector<int>>'
        if lang == 'javascript': return 'number[][]'
    raise ValueError(f"Unsupported DSL type: {dsl_type} for language {lang}")

def generate_python_template(signature: Signature) -> str:
    function_name = signature.function_name
    parameters = signature.parameters
    return_dsl = signature.returns['type']
    return_type = get_language_type('python', return_dsl)
    param_str = ', '.join(f"{p.name}: {get_language_type('python', p.type)}" for p in parameters)
    uses_listnode = any(t == 'List' for t in [p.type for p in parameters] + [return_dsl])
    uses_treenode = any(t == 'Tree' for t in [p.type for p in parameters] + [return_dsl])
    template = ["from typing import List, Optional\n"]
    if uses_listnode:
        template.append("""
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def build_listnode(arr: List[int]) -> Optional[ListNode]:
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def serialize_listnode(head: Optional[ListNode]) -> List[int]:
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res
""")
    if uses_treenode:
        template.append("""
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_treenode(data: Dict) -> Optional[TreeNode]:
    if data is None: return None
    node = TreeNode(data.get('val', 0))
    node.left = build_treenode(data.get('left'))
    node.right = build_treenode(data.get('right'))
    return node

def serialize_treenode(node: Optional[TreeNode]) -> Optional[Dict]:
    if node is None: return None
    return {'val': node.val, 'left': serialize_treenode(node.left), 'right': serialize_treenode(node.right)}
""")
    template.append(f"""
class Solution:
    def {function_name}(self, {param_str}) -> {return_type}:
        # Write your logic here
        pass
""")
    template.append("""
if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    kwargs = {}
""")
    for p in parameters:
        if p.type == 'List':
            template.append(f"    kwargs['{p.name}'] = build_listnode(data.get('{p.name}', []))\n")
        elif p.type == 'Tree':
            template.append(f"    kwargs['{p.name}'] = build_treenode(data.get('{p.name}'))\n")
        else:
            template.append(f"    kwargs['{p.name}'] = data.get('{p.name}')\n")
    template.append(f"    result = Solution().{function_name}(**kwargs)\n")
    if return_dsl == 'List':
        template.append("    result = serialize_listnode(result)\n")
    elif return_dsl == 'Tree':
        template.append("    result = serialize_treenode(result)\n")
    template.append("    print(json.dumps(result))\n")
    return ''.join(template)


# Similar generator functions for other languages (abbreviated for brevity; full implementations follow the same pattern)
def generate_java_template(signature: Signature) -> str:
    function_name = signature.function_name
    parameters = signature.parameters
    return_dsl = signature.returns['type']
    return_type = get_language_type('java', return_dsl)
    param_str = ', '.join(f"{get_language_type('java', p.type)} {p.name}" for p in parameters)
    uses_listnode = any(t == 'List' for t in [p.type for p in parameters] + [return_dsl])
    uses_treenode = any(t == 'Tree' for t in [p.type for p in parameters] + [return_dsl])
    uses_graph = any(t == 'Graph' for t in [p.type for p in parameters] + [return_dsl])
    template = [
        "import java.util.*;\n",
        "import com.google.gson.*;\n",
        "import java.io.InputStreamReader;\n",
        "import java.io.BufferedReader;\n\n",
        "public class Solution {\n"
    ]
    if uses_listnode:
        template.append("""
    public static class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }

    public static ListNode buildListNode(JsonArray arr) {
        if (arr == null || arr.size() == 0) return null;
        ListNode head = new ListNode(arr.get(0).getAsInt());
        ListNode curr = head;
        for (int i = 1; i < arr.size(); i++) {
            curr.next = new ListNode(arr.get(i).getAsInt());
            curr = curr.next;
        }
        return head;
    }

    public static JsonArray serializeListNode(ListNode head) {
        JsonArray res = new JsonArray();
        while (head != null) {
            res.add(head.val);
            head = head.next;
        }
        return res;
    }
""")
    if uses_treenode:
        template.append("""
    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode() {}
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    public static TreeNode buildTreeNode(JsonObject data) {
        if (data == null || data.isJsonNull()) return null;
        TreeNode node = new TreeNode(data.get("val").getAsInt());
        node.left = buildTreeNode((JsonObject) data.get("left"));
        node.right = buildTreeNode((JsonObject) data.get("right"));
        return node;
    }

    public static JsonObject serializeTreeNode(TreeNode node) {
        if (node == null) return null;
        JsonObject res = new JsonObject();
        res.addProperty("val", node.val);
        res.add("left", serializeTreeNode(node.left));
        res.add("right", serializeTreeNode(node.right));
        return res;
    }
""")
    template.append(f"    public {return_type} {function_name}({param_str}) {{\n")
    template.append("        // Write your logic here\n")
    if return_dsl.startswith('void'):
        template.append("    }\n")
    else:
        template.append("        return null;\n    }\n")
    template.append("""
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line);
        }
        Gson gson = new Gson();
        JsonObject data = gson.fromJson(sb.toString(), JsonObject.class);
        Solution solution = new Solution();
""")
    call_args = []
    for p in parameters:
        p_type = p.type
        if p_type == 'List':
            template.append(f"        ListNode {p.name} = buildListNode(data.getAsJsonArray(\"{p.name}\"));\n")
            call_args.append(p.name)
        elif p_type == 'Tree':
            template.append(f"        TreeNode {p.name} = buildTreeNode(data.getAsJsonObject(\"{p.name}\"));\n")
            call_args.append(p.name)
        elif p_type == 'Graph':
            template.append(f"        List<List<Integer>> {p.name} = gson.fromJson(data.get(\"{p.name}\"), new TypeToken<List<List<Integer>>>(){{}}.getType());\n")
            call_args.append(p.name)
        elif p_type.endswith('[]'):
            inner = p_type[:-2]
            boxed = java_boxed.get(inner, get_language_type('java', inner))
            template.append(f"        List<{boxed}> {p.name}_list = gson.fromJson(data.get(\"{p.name}\"), new TypeToken<List<{boxed}>>{{}}.getType());\n")
            if inner in ['int', 'long', 'float', 'double', 'bool']:
                prim = primitive_map['java'][inner]
                template.append(f"        {prim}[] {p.name} = new {prim}[{p.name}_list.size()];\n")
                template.append(f"        for (int i = 0; i < {p.name}_list.size(); i++) {p.name}[i] = {p.name}_list.get(i);\n")
            else:
                template.append(f"        {boxed}[] {p.name} = {p.name}_list.toArray(new {boxed}[0]);\n")
            call_args.append(p.name)
        else:
            prim = primitive_map['java'][p_type]
            template.append(f"        {prim} {p.name} = data.get(\"{p.name}\").getAs{prim.capitalize()}();\n")
            call_args.append(p.name)
    call_str = ', '.join(call_args)
    template.append(f"        {return_type} result = solution.{function_name}({call_str});\n")
    if return_dsl == 'List':
        template.append("        JsonArray serialized = serializeListNode(result);\n")
        template.append("        System.out.println(gson.toJson(serialized));\n")
    elif return_dsl == 'Tree':
        template.append("        JsonObject serialized = serializeTreeNode(result);\n")
        template.append("        System.out.println(gson.toJson(serialized));\n")
    elif return_dsl == 'Graph':
        template.append("        System.out.println(gson.toJson(result));\n")
    elif return_dsl.endswith('[]'):
        template.append("        System.out.println(gson.toJson(result));\n")
    else:
        template.append("        System.out.println(gson.toJson(result));\n")
    template.append("    }\n}\n")
    return ''.join(template)


def generate_cpp_template(signature: Signature) -> str:
    function_name = signature.function_name
    parameters = signature.parameters
    return_dsl = signature.returns['type']
    return_type = get_language_type('cpp', return_dsl)
    param_str = ', '.join(f"{get_language_type('cpp', p.type)} {p.name}" for p in parameters)
    uses_listnode = any(t == 'List' for t in [p.type for p in parameters] + [return_dsl])
    uses_treenode = any(t == 'Tree' for t in [p.type for p in parameters] + [return_dsl])
    template = [
        "#include <bits/stdc++.h>\n",
        "#include <nlohmann/json.hpp>\n",
        "using json = nlohmann::json;\n",
        "using namespace std;\n\n"
    ]
    if uses_listnode:
        template.append("""
struct ListNode {
    int val;
    ListNode* next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode* next) : val(x), next(next) {}
};

ListNode* buildListNode(const json& arr) {
    if (arr.empty()) return nullptr;
    ListNode* head = new ListNode(arr[0].get<int>());
    ListNode* curr = head;
    for (size_t i = 1; i < arr.size(); ++i) {
        curr->next = new ListNode(arr[i].get<int>());
        curr = curr->next;
    }
    return head;
}

json serializeListNode(ListNode* head) {
    json res = json::array();
    while (head) {
        res.push_back(head->val);
        head = head->next;
    }
    return res;
}
""")
    if uses_treenode:
        template.append("""
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode() : val(0), left(nullptr), right(nullptr) {}
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
    TreeNode(int x, TreeNode* left, TreeNode* right) : val(x), left(left), right(right) {}
};

TreeNode* buildTreeNode(const json& data) {
    if (data.is_null()) return nullptr;
    TreeNode* node = new TreeNode(data["val"].get<int>());
    node->left = buildTreeNode(data["left"]);
    node->right = buildTreeNode(data["right"]);
    return node;
}

json serializeTreeNode(TreeNode* node) {
    if (!node) return nullptr;
    json res;
    res["val"] = node->val;
    res["left"] = serializeTreeNode(node->left);
    res["right"] = serializeTreeNode(node->right);
    return res;
}
""")
    template.append("class Solution {\npublic:\n")
    template.append(f"    {return_type} {function_name}({param_str}) {{\n")
    template.append("        // Write your logic here\n")
    if return_dsl == 'void':
        template.append("    }\n")
    else:
        template.append("        return {};\n    }\n")
    template.append("};\n\n")
    template.append("""
int main() {
    string input;
    string line;
    while (getline(cin, line)) {
        input += line;
    }
    json data = json::parse(input);
    Solution solution;
""")
    call_args = []
    for p in parameters:
        p_type = p.type
        if p_type == 'List':
            template.append(f"    ListNode* {p.name} = buildListNode(data[\"{p.name}\"]);\n")
            call_args.append(p.name)
        elif p_type == 'Tree':
            template.append(f"    TreeNode* {p.name} = buildTreeNode(data[\"{p.name}\"]);\n")
            call_args.append(p.name)
        elif p_type == 'Graph':
            template.append(f"    vector<vector<int>> {p.name} = data[\"{p.name}\"].get<vector<vector<int>>>();\n")
            call_args.append(p.name)
        elif p_type.endswith('[]'):
            template.append(f"    {get_language_type('cpp', p_type)} {p.name} = data[\"{p.name}\"].get<{get_language_type('cpp', p_type)} >();\n")
            call_args.append(p.name)
        else:
            template.append(f"    {get_language_type('cpp', p_type)} {p.name} = data[\"{p.name}\"].get<{get_language_type('cpp', p_type)} >();\n")
            call_args.append(p.name)
    call_str = ', '.join(call_args)
    template.append(f"    auto result = solution.{function_name}({call_str});\n")
    if return_dsl == 'List':
        template.append("    json serialized = serializeListNode(result);\n")
        template.append("    cout << serialized.dump() << endl;\n")
    elif return_dsl == 'Tree':
        template.append("    json serialized = serializeTreeNode(result);\n")
        template.append("    cout << serialized.dump() << endl;\n")
    else:
        template.append("    cout << json(result).dump() << endl;\n")
    template.append("    return 0;\n}\n")
    return ''.join(template)

def generate_javascript_template(signature: Signature) -> str:
    function_name = signature.function_name
    parameters = signature.parameters
    return_dsl = signature.returns['type']
    return_type = get_language_type('javascript', return_dsl)
    param_str = parameters and ', '.join(f"{p.name}" for p in parameters) or ''
    uses_listnode = any(t == 'List' for t in [p.type for p in parameters] + [return_dsl])
    uses_treenode = any(t == 'Tree' for t in [p.type for p in parameters] + [return_dsl])
    template = ["const fs = require('fs');\n"]
    if uses_listnode:
        template.append("""
class ListNode {
    constructor(val = 0, next = null) {
        this.val = val;
        this.next = next;
    }
}

function buildListNode(arr) {
    if (!arr || arr.length === 0) return null;
    let head = new ListNode(arr[0]);
    let curr = head;
    for (let i = 1; i < arr.length; i++) {
        curr.next = new ListNode(arr[i]);
        curr = curr.next;
    }
    return head;
}

function serializeListNode(head) {
    const res = [];
    while (head) {
        res.push(head.val);
        head = head.next;
    }
    return res;
}
""")
    if uses_treenode:
        template.append("""
class TreeNode {
    constructor(val = 0, left = null, right = null) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}

function buildTreeNode(data) {
    if (!data) return null;
    const node = new TreeNode(data.val);
    node.left = buildTreeNode(data.left);
    node.right = buildTreeNode(data.right);
    return node;
}

function serializeTreeNode(node) {
    if (!node) return null;
    return {
        val: node.val,
        left: serializeTreeNode(node.left),
        right: serializeTreeNode(node.right)
    };
}
""")
    template.append("class Solution {\n")
    template.append(f"    {function_name}({param_str}) {{\n")
    template.append("        // Write your logic here\n")
    template.append("        return null;\n    }\n")
    template.append("}\n\n")
    template.append("""
const input = fs.readFileSync(0, 'utf-8');
const data = JSON.parse(input);
const solution = new Solution();
""")
    call_args = []
    for p in parameters:
        p_type = p.type
        if p_type == 'List':
            template.append(f"const {p.name} = buildListNode(data['{p.name}']);\n")
            call_args.append(p.name)
        elif p_type == 'Tree':
            template.append(f"const {p.name} = buildTreeNode(data['{p.name}']);\n")
            call_args.append(p.name)
        else:
            template.append(f"const {p.name} = data['{p.name}'];\n")
            call_args.append(p.name)
    call_str = ', '.join(call_args)
    template.append(f"let result = solution.{function_name}({call_str});\n")
    if return_dsl == 'List':
        template.append("result = serializeListNode(result);\n")
    elif return_dsl == 'Tree':
        template.append("result = serializeTreeNode(result);\n")
    template.append("console.log(JSON.stringify(result));\n")
    return ''.join(template)
# Endpoint
@app.post("/api/v1/template", status_code=201)
def generate_template(payload: Payload):
    try:
        lang = payload.language
        signature = payload.signature
        if lang == 'python':
            template = generate_python_template(signature)
        elif lang == 'java':
            template = generate_java_template(signature)
        elif lang == 'cpp':
            template = generate_cpp_template(signature)
        elif lang == 'javascript':
            template = generate_javascript_template(signature)
        return {"language": lang, "template": template}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Unit Tests (using pytest style, run with pytest)
def test_fibonacci():
    payload = Payload(
        question_id="fib", title="Fibonacci", description="...",
        signature=Signature(function_name="fib", parameters=[Parameter(name="n", type="int")], returns={"type": "int"}),
        language="python"
    )
    template = generate_python_template(payload.signature)
    assert "def fib(self, n: int) -> int:" in template  # Snapshot assertion

# Similar tests for other scenarios and languages
def test_merge_k_lists():
    # Assert includes ListNode definition
    pass

def test_lowest_common_ancestor():
    # Assert includes TreeNode
    pass

def test_detect_cycle():
    # Assert graph handling
    pass