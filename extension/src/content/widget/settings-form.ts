import { getUserSettings, setUserSettings, type FitPreference } from '../../shared/storage';
import { el, setStyles } from './dom';
import { fontFamily, theme } from './theme';

type SettingsFormOptions = {
  readonly onSaved: () => void;
};

function parseOptionalNumber(value: string): number | undefined {
  const trimmed = value.trim();
  if (!trimmed) return undefined;
  const n = Number(trimmed);
  if (!Number.isFinite(n) || n <= 0) return undefined;
  return n;
}

function normalizeFitPreference(value: string): FitPreference {
  if (value === 'fitted' || value === 'relaxed') return value;
  return 'regular';
}

function inputStyles(): Partial<CSSStyleDeclaration> {
  return {
    width: '100%',
    padding: '8px 10px',
    borderRadius: '10px',
    border: `1px solid ${theme.inputBorder}`,
    background: theme.inputBg,
    color: theme.text,
    outline: 'none',
    fontFamily,
    fontSize: '13px',
  };
}

function labelStyles(): Partial<CSSStyleDeclaration> {
  return {
    display: 'grid',
    gap: '6px',
    fontSize: '12px',
    color: theme.muted,
  };
}

export async function createSettingsForm(
  opts: SettingsFormOptions,
): Promise<HTMLElement> {
  const settings = await getUserSettings();

  const wrap = el('div');
  setStyles(wrap, { display: 'grid', gap: '10px' });

  const grid = el('div');
  setStyles(grid, {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, minmax(0, 1fr))',
    gap: '10px',
  });

  const bustLabel = el('label');
  setStyles(bustLabel, labelStyles());
  bustLabel.appendChild(el('span', { text: 'Bust (in)' }));
  const bust = el('input') as HTMLInputElement;
  bust.inputMode = 'decimal';
  bust.placeholder = 'e.g. 36';
  bust.value = settings.measurements.bustIn?.toString() ?? '';
  setStyles(bust, inputStyles());
  bustLabel.appendChild(bust);

  const waistLabel = el('label');
  setStyles(waistLabel, labelStyles());
  waistLabel.appendChild(el('span', { text: 'Waist (in)' }));
  const waist = el('input') as HTMLInputElement;
  waist.inputMode = 'decimal';
  waist.placeholder = 'e.g. 29';
  waist.value = settings.measurements.waistIn?.toString() ?? '';
  setStyles(waist, inputStyles());
  waistLabel.appendChild(waist);

  const hipsLabel = el('label');
  setStyles(hipsLabel, labelStyles());
  hipsLabel.appendChild(el('span', { text: 'Hips (in)' }));
  const hips = el('input') as HTMLInputElement;
  hips.inputMode = 'decimal';
  hips.placeholder = 'e.g. 39';
  hips.value = settings.measurements.hipsIn?.toString() ?? '';
  setStyles(hips, inputStyles());
  hipsLabel.appendChild(hips);

  grid.appendChild(bustLabel);
  grid.appendChild(waistLabel);
  grid.appendChild(hipsLabel);

  const prefLabel = el('label');
  setStyles(prefLabel, labelStyles());
  prefLabel.appendChild(el('span', { text: 'Fit preference' }));
  const pref = el('select') as HTMLSelectElement;
  for (const p of ['regular', 'fitted', 'relaxed'] as const) {
    const o = el('option') as HTMLOptionElement;
    o.value = p;
    o.textContent = p;
    pref.appendChild(o);
  }
  pref.value = settings.fitPreference;
  setStyles(pref, inputStyles());
  prefLabel.appendChild(pref);

  const actions = el('div');
  setStyles(actions, { display: 'flex', gap: '8px' });

  const save = el('button', { text: 'Save' }) as HTMLButtonElement;
  setStyles(save, {
    flex: '1',
    padding: '9px 10px',
    borderRadius: '10px',
    border: `1px solid ${theme.btnBorder}`,
    background: theme.btnBg,
    color: theme.text,
    cursor: 'pointer',
    fontFamily,
    fontSize: '13px',
  });

  const note = el('div', { text: 'Saved locally (no accounts).' });
  setStyles(note, { fontSize: '11px', color: theme.muted, marginTop: '2px' });

  save.addEventListener('click', async () => {
    await setUserSettings({
      measurements: {
        bustIn: parseOptionalNumber(bust.value),
        waistIn: parseOptionalNumber(waist.value),
        hipsIn: parseOptionalNumber(hips.value),
      },
      fitPreference: normalizeFitPreference(pref.value),
    });
    opts.onSaved();
  });

  actions.appendChild(save);

  wrap.appendChild(grid);
  wrap.appendChild(prefLabel);
  wrap.appendChild(actions);
  wrap.appendChild(note);

  return wrap;
}

