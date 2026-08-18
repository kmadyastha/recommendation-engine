import type { PreferenceFormValues } from "@/lib/types";
import { BUDGET_LABELS } from "@/lib/types";

interface PreferenceSidebarProps {
  values: PreferenceFormValues;
  onEdit: () => void;
}

export function PreferenceSidebar({ values, onEdit }: PreferenceSidebarProps) {
  return (
    <aside className="w-full md:w-1/3 lg:w-1/4">
      <div className="sticky top-[104px] flex flex-col gap-sm rounded-xl border border-surface-container-high bg-surface-container-low p-sm">
        <h2 className="text-title-md text-on-surface">Your Search</h2>
        <div className="mt-sm flex flex-col gap-xs">
          <SidebarRow
            icon="location_on"
            label="Location"
            value={values.location || "—"}
          />
          <SidebarRow
            icon="ramen_dining"
            label="Cuisine"
            value={values.cuisine || "Any cuisine"}
          />
          <SidebarRow
            icon="payments"
            label="Budget"
            value={BUDGET_LABELS[values.budget]}
          />
          {values.min_rating > 0 && (
            <SidebarRow
              icon="star"
              label="Min rating"
              value={`${values.min_rating.toFixed(1)}+`}
            />
          )}
          {values.additional_preferences && (
            <SidebarRow
              icon="mood"
              label="Vibe"
              value={values.additional_preferences}
            />
          )}
        </div>
        <button
          type="button"
          onClick={onEdit}
          className="mt-md flex w-full items-center justify-center gap-xs rounded-full border border-surface-container-high bg-transparent py-xs text-body-sm text-on-surface transition-colors hover:bg-surface-container"
        >
          <span className="material-symbols-outlined text-[18px]">edit</span>
          Edit search
        </button>
      </div>
    </aside>
  );
}

function SidebarRow({
  icon,
  label,
  value,
}: {
  icon: string;
  label: string;
  value: string;
}) {
  return (
    <div className="mt-xs flex items-start gap-xs">
      <span className="material-symbols-outlined mt-1 text-[18px] text-secondary-container">
        {icon}
      </span>
      <div>
        <span className="block text-label-caps uppercase tracking-wider text-on-surface-variant">
          {label}
        </span>
        <span className="text-body-sm text-on-surface">{value}</span>
      </div>
    </div>
  );
}
