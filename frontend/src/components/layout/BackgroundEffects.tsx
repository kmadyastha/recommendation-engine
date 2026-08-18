export function BackgroundEffects() {
  return (
    <>
      <div className="pointer-events-none absolute inset-0 z-0 bg-gradient-to-b from-primary-container/5 via-transparent to-tertiary-container/5" />
      <div className="pointer-events-none absolute left-1/4 top-0 z-0 h-96 w-96 rounded-full bg-primary-container opacity-10 mix-blend-screen blur-[120px] filter" />
      <div className="pointer-events-none absolute bottom-1/4 right-1/4 z-0 h-[500px] w-[500px] rounded-full bg-tertiary-container opacity-10 mix-blend-screen blur-[150px] filter" />
    </>
  );
}
