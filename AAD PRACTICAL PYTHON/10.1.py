from flask import Flask, render_template, request
import heapq
app = Flask(__name__)
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq
def build_huffman_tree(char_freq):
    heap = [Node(freq, char) for char, freq in char_freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, None, left, right)
        heapq.heappush(heap, merged)
    return heap[0]
def generate_huffman_codes(node, prefix='', codebook={}):
    if node.char:
        codebook[node.char] = prefix
    else:
        generate_huffman_codes(node.left, prefix + '0', codebook)
        generate_huffman_codes(node.right, prefix + '1', codebook)
    return codebook
def encode(text, codebook):
    return ''.join([codebook[char] for char in text])
def decode(encoded_text, huffman_tree):
    decoded_text = []
    node = huffman_tree
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.char:
            decoded_text.append(node.char)
            node = huffman_tree
    return ''.join(decoded_text)
@app.route('/', methods=['GET', 'POST'])
def huffman():
    if request.method == 'POST':
        characters = request.form.getlist('characters')
        frequencies = list(map(float, request.form.getlist('frequencies')))
        char_freq = {characters[i]: frequencies[i] for i in range(len(characters))}
        huffman_tree = build_huffman_tree(char_freq)
        codebook = generate_huffman_codes(huffman_tree)
        text_to_encode = request.form['text_to_encode']
        encoded_text = encode(text_to_encode, codebook)
        text_to_decode = request.form['text_to_decode']
        decoded_text = decode(text_to_decode, huffman_tree)
        return render_template('prac10_result.html', encoded_text=encoded_text, decoded_text=decoded_text, codebook=codebook)
    return render_template('prac10.html')
if __name__ == '__main__':
    app.run(debug=True)
