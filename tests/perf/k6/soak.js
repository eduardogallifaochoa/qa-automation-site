import http from 'k6/http';
import { check, group, sleep } from 'k6';

export const options = {
  vus: 20,
  duration: '12h',
  thresholds: {
    'http_req_duration{name:login}': ['p(95)<500'],
    'http_req_duration{name:contact}': ['p(95)<500'],
    'http_req_failed': ['rate<0.01'],
  },
  summaryTrendStats: ['avg', 'min', 'med', 'p(90)', 'p(95)', 'max'],
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

  // Keep steady pace. Soak is about stability under sustained load.
  sleep(1);
}
