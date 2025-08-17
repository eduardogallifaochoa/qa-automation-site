// Stress test: ramp VUs up in steps to find the breaking point.
// All code comments in English (as requested).
import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '1m', target: 10 },   // warm-up
    { duration: '1m', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '1m', target: 200 },
    { duration: '1m', target: 300 },  // push harder; adjust if your box cries
    { duration: '1m', target: 0 },    // ramp-down to observe recovery
  ],
  thresholds: {
    'http_req_duration{name:login}': ['p(95)<500'],
    'http_req_duration{name:contact}': ['p(95)<500'],
    'http_req_failed': ['rate<0.01'],
  },
  summaryTrendStats: ['avg', 'min', 'med', 'p(90)', 'p(95)', 'max'],
  gracefulStop: '30s',
};

const BASE_URL = __ENV.BASE_URL || 'http://host.docker.internal:8000';

export default function () {
  const headers = { 'Content-Type': 'application/json' };

  group('login', () => {
    const res = http.post(
      `${BASE_URL}/api/login`,
      JSON.stringify({ username: 'admin', password: '1234' }),
      { headers, tags: { name: 'login' } }
    );
    check(res, { 'status is 200': (r) => r.status === 200 });
  });

  group('contact', () => {
    const res = http.post(
      `${BASE_URL}/api/contact`,
      JSON.stringify({ name: 'Eddie', email: 'a@b.com', message: 'Hello from QA site!' }),
      { headers, tags: { name: 'contact' } }
    );
    check(res, { 'status is 200': (r) => r.status === 200 });
  });

  // Keep iterations fast so stress comes from concurrency + pace.
  sleep(0.2);
}
