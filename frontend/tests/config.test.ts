import { describe, expect, it } from 'vitest';
import { CONFIG } from '../src/lib/config';

describe('integration config defaults', () => {
  it('uses localhost defaults for local development', () => {
    expect(CONFIG.tastyigniter.baseUrl).toBe('http://localhost:8081');
    expect(CONFIG.hievents.baseUrl).toBe('http://localhost:8082');
  });
});
