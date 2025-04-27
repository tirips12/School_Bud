import React, { Suspense, lazy } from 'react';
import { createRoot } from 'react-dom/client';

const PerCourseActivity = lazy(() => import('./AnalyticsDashboard').then(m => ({ default: m.PerCourseActivity })));
const GithubAnalytics = lazy(() => import('./GithubAnalytics'));
const ActivityLog = lazy(() => import('./AnalyticsDashboard').then(m => ({ default: m.ActivityLog })));
const LanguageDistribution = lazy(() => import('./LanguageDistribution'));

// Mount PerCourseActivity
const perCourseDiv = document.getElementById('react-per-course-activity');
if (perCourseDiv) {
  const statsScript = document.getElementById('per-course-stats');
  let stats = [];
  if (statsScript) {
    try {
      stats = JSON.parse(statsScript.textContent);
    } catch (e) {
      console.error('Failed to parse per-course stats:', e);
    }
  }
  createRoot(perCourseDiv).render(
    <Suspense fallback={<div>Loading Course Activity...</div>}>
      <PerCourseActivity stats={stats} />
    </Suspense>
  );
}

// Mount GithubAnalytics
const githubDiv = document.getElementById('react-github-analytics');
if (githubDiv) {
  createRoot(githubDiv).render(
    <Suspense fallback={<div>Loading GitHub Analytics...</div>}>
      <GithubAnalytics />
    </Suspense>
  );
}

// Mount ActivityLog
const activityDiv = document.getElementById('react-activity-log');
if (activityDiv) {
  createRoot(activityDiv).render(
    <Suspense fallback={<div>Loading Activity Log...</div>}>
      <ActivityLog />
    </Suspense>
  );
}

// Mount LanguageDistribution
const languageDiv = document.getElementById('react-language-distribution');
if (languageDiv) {
  createRoot(languageDiv).render(
    <Suspense fallback={<div>Loading Language Distribution...</div>}>
      <LanguageDistribution />
    </Suspense>
  );
}
