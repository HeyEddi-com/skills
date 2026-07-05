# Examples

## Before (bad)

```vue
<div style="padding: 16px; color: #333">...</div>
```

## After (good)

```vue
<div class="section">...</div>
```

```css
.section {
  padding: var(--size-3);
  color: var(--text-1);
}
```
