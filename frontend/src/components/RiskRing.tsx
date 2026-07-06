interface Props {
  value: number;
  tone: "ok" | "warn" | "danger";
}

const TONE: Record<Props["tone"], string> = {
  ok: "var(--ok)",
  warn: "var(--warn)",
  danger: "var(--danger)",
};

const SIZE = 200;
const STROKE = 20;
const R = (SIZE - STROKE) / 2;
const C = 2 * Math.PI * R;

export function RiskRing({ value, tone }: Props) {
  const clamped = Math.max(0, Math.min(1, value));
  const dash = C * clamped;

  return (
    <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="ring" role="img"
      aria-label={`Risk ${(clamped * 100).toFixed(0)} percent`}>
      <circle cx={SIZE / 2} cy={SIZE / 2} r={R} fill="none"
        stroke="var(--surface-2)" strokeWidth={STROKE} />
      <circle cx={SIZE / 2} cy={SIZE / 2} r={R} fill="none"
        stroke={TONE[tone]} strokeWidth={STROKE} strokeLinecap="round"
        strokeDasharray={`${dash} ${C}`}
        transform={`rotate(-90 ${SIZE / 2} ${SIZE / 2})`}
        style={{ transition: "stroke-dasharray 800ms var(--ease-soft), stroke 400ms ease" }} />
      <text x="50%" y="47%" textAnchor="middle" className="ring__num" fill="var(--ink)">
        {(clamped * 100).toFixed(0)}<tspan className="ring__pct">%</tspan>
      </text>
      <text x="50%" y="63%" textAnchor="middle" className="ring__cap" fill="var(--ink-3)">
        estimated risk
      </text>
    </svg>
  );
}
