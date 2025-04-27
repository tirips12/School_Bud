import React from 'react';
import { createRoot } from 'react-dom/client';
import MarkdownRenderer from './components/MarkdownRenderer';

// Mount for all question content blocks (home page)
const questionDivs = document.querySelectorAll('div[id^="react-question-content-"]');
questionDivs.forEach(div => {
  const questionId = div.id.replace('react-question-content-', '');
  const script = document.getElementById(`react-question-content-data-${questionId}`);
  let content = '';
  if (script) {
    try {
      content = JSON.parse(script.textContent);
    } catch (e) {
      content = script.textContent || '';
    }
  }
  createRoot(div).render(<MarkdownRenderer>{content}</MarkdownRenderer>);
});

// Mount for single question content (question detail page)
const questionDiv = document.getElementById('react-question-content');
if (questionDiv) {
  const script = document.getElementById('react-question-content-data');
  let content = '';
  if (script) {
    try {
      content = JSON.parse(script.textContent);
    } catch (e) {
      content = script.textContent || '';
    }
  }
  createRoot(questionDiv).render(<MarkdownRenderer>{content}</MarkdownRenderer>);
}

// Mount for each answer content
const answerDivs = document.querySelectorAll('[id^="react-answer-content-"]');
answerDivs.forEach(div => {
  const answerId = div.id.replace('react-answer-content-', '');
  const script = document.getElementById(`react-answer-content-data-${answerId}`);
  let content = '';
  if (script) {
    try {
      content = JSON.parse(script.textContent);
    } catch (e) {
      content = script.textContent || '';
    }
  }
  console.log('Mounting answer', { answerId, script, content });
  if (!content) content = '[No content found for answer ' + answerId + ']';
  createRoot(div).render(<MarkdownRenderer>{content}</MarkdownRenderer>);
});

// Mount for each GitHub project comment
const githubCommentDivs = document.querySelectorAll('div[id^="react-github-comment-"]');
githubCommentDivs.forEach(div => {
  const commentId = div.id.replace('react-github-comment-', '');
  const script = document.getElementById(`react-github-comment-data-${commentId}`);
  let content = '';
  if (script) {
    try {
      content = JSON.parse(script.textContent);
    } catch (e) {
      content = script.textContent || '';
    }
  }
  console.log('Mounting GitHub comment', { commentId, script, content });
  if (!content) content = '[No content found for comment ' + commentId + ']';
  createRoot(div).render(<MarkdownRenderer>{content}</MarkdownRenderer>);
});

// Mount for each project discussion comment
const discussionCommentDivs = document.querySelectorAll('div[id^="react-discussion-comment-"]');
discussionCommentDivs.forEach(div => {
  const commentId = div.id.replace('react-discussion-comment-', '');
  const script = document.getElementById(`react-discussion-comment-data-${commentId}`);
  let content = '';
  if (script) {
    try {
      content = JSON.parse(script.textContent);
    } catch (e) {
      content = script.textContent || '';
    }
  }
  if (!content) content = '[No content found for discussion comment ' + commentId + ']';
  createRoot(div).render(<MarkdownRenderer>{content}</MarkdownRenderer>);
});
