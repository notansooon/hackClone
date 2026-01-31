export function el<K extends keyof HTMLElementTagNameMap>(
  tag: K,
  init?: {
    readonly text?: string;
    readonly className?: string;
  },
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (init?.text !== undefined) node.textContent = init.text;
  if (init?.className) node.className = init.className;
  return node;
}

export function byId<T extends HTMLElement>(id: string): T {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing element #${id}`);
  return node as T;
}

export function setStyles(
  node: HTMLElement,
  styles: Partial<CSSStyleDeclaration>,
): void {
  Object.assign(node.style, styles);
}

