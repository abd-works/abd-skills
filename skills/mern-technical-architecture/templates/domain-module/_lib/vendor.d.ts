// =============================================================================
// Ambient module stubs for template compilation.
// In a real project, these come from node_modules via npm install.
// Delete this _lib/ folder when using real packages.
// =============================================================================

// --- zod ---
declare module 'zod' {
  interface ZodType {
    parse(data: unknown): any;
    safeParse(data: unknown): { success: boolean; data?: any; error?: { issues: Array<{ message: string }> } };
    optional(): ZodType;
  }

  interface ZodString extends ZodType {
    min(len: number, msg?: string): ZodString;
    max(len: number, msg?: string): ZodString;
    uuid(msg?: string): ZodString;
    regex(pattern: RegExp, msg?: string): ZodString;
    length(len: number, msg?: string): ZodString;
  }

  interface ZodNumber extends ZodType {
    min(val: number, msg?: string): ZodNumber;
    max(val: number, msg?: string): ZodNumber;
  }

  interface ZodDate extends ZodType {}

  interface ZodEnum extends ZodType {}

  interface ZodObject extends ZodType {}

  interface ZodCoerce {
    date(): ZodDate;
    number(): ZodNumber;
    string(): ZodString;
  }

  const z: {
    string(): ZodString;
    number(): ZodNumber;
    date(): ZodDate;
    enum(values: readonly string[]): ZodEnum;
    object(shape: Record<string, ZodType>): ZodObject;
    coerce: ZodCoerce;
  };

  export { z, ZodType, ZodString, ZodNumber, ZodDate, ZodEnum, ZodObject, ZodCoerce };
  export default z;
}

// --- mongodb ---
declare module 'mongodb' {
  interface FindCursor<T = any> {
    toArray(): Promise<T[]>;
  }

  interface Collection<T = any> {
    find(filter?: Record<string, any>): FindCursor<T>;
    insertOne(doc: T): Promise<{ insertedId: string }>;
    updateOne(filter: Record<string, any>, update: Record<string, any>): Promise<{ modifiedCount: number }>;
    deleteOne(filter: Record<string, any>): Promise<{ deletedCount: number }>;
  }

  interface Db {
    collection<T = any>(name: string): Collection<T>;
  }

  export { Db, Collection, FindCursor };
}

// --- express ---
declare module 'express' {
  interface Request {
    user?: { enterpriseId: string; [key: string]: any };
    query: Record<string, string | undefined>;
    params: Record<string, string>;
    body: any;
  }

  interface Response {
    json(data: any): Response;
    status(code: number): Response;
    send(body?: any): Response;
  }

  type RequestHandler = (req: Request, res: Response, next?: () => void) => any;

  interface Router {
    get(path: string, ...handlers: RequestHandler[]): Router;
    post(path: string, ...handlers: RequestHandler[]): Router;
    put(path: string, ...handlers: RequestHandler[]): Router;
    delete(path: string, ...handlers: RequestHandler[]): Router;
    use(...handlers: RequestHandler[]): Router;
  }

  function Router(): Router;

  export { Request, Response, Router, RequestHandler };
}

// --- react ---
declare module 'react' {
  function useState<T>(initial: T | (() => T)): [T, (value: T | ((prev: T) => T)) => void];
  function useEffect(effect: () => void | (() => void), deps?: any[]): void;
  function useCallback<T extends (...args: any[]) => any>(callback: T, deps: any[]): T;
  function useMemo<T>(factory: () => T, deps: any[]): T;
  function useRef<T>(initial: T): { current: T };

  type FC<P = {}> = (props: P) => JSX.Element | null;
  type ReactNode = JSX.Element | string | number | null | undefined | boolean | ReactNode[];

  const React: {
    useState: typeof useState;
    useEffect: typeof useEffect;
    useCallback: typeof useCallback;
    useMemo: typeof useMemo;
    useRef: typeof useRef;
  };

  export { useState, useEffect, useCallback, useMemo, useRef, FC, ReactNode };
  export default React;
}

// --- react/jsx-runtime ---
declare module 'react/jsx-runtime' {
  export function jsx(type: any, props: any, key?: string): JSX.Element;
  export function jsxs(type: any, props: any, key?: string): JSX.Element;
  export const Fragment: symbol;
}

// --- JSX namespace ---
declare namespace JSX {
  interface Element {}
  interface IntrinsicElements {
    [elemName: string]: any;
  }
}
