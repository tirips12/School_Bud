import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneLight } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from 'react-bootstrap';

function CodeBlock({ inline, className, children, ...props }) {
  const [copied, setCopied] = useState(false);
  const match = /language-(\w+)/.exec(className || '');
  const code = String(children).replace(/\n$/, '');

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      setCopied(false);
    }
  };

  if (inline) {
    return <code className={className} {...props}>{children}</code>;
  }

  return (
    <div style={{ marginBottom: '0.5em' }}>
      <Button
        variant="outline-secondary"
        size="sm"
        style={{ marginBottom: 4 }}
        onClick={handleCopy}
      >
        {copied ? 'Copied!' : 'Copy'}
      </Button>
      <SyntaxHighlighter
        style={oneLight}
        language={match ? match[1] : ''}
        PreTag="div"
        customStyle={{ borderRadius: '8px', marginBottom: '0', fontSize: '1em' }}
        {...props}
      >
        {code}
      </SyntaxHighlighter>
    </div>
  );
}

export default function MarkdownRenderer({ children }) {
  return (
    <ReactMarkdown
      components={{
        code: CodeBlock
      }}
      skipHtml
    >
      {children}
    </ReactMarkdown>
  );
}
