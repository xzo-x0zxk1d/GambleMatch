export default function Background() {
  return (
    <div className="bg-root" aria-hidden>
      {/* Deep space base */}
      <div className="bg-base" />

      {/* Radial spotlight top-left */}
      <div className="bg-spot bg-spot-1" />

      {/* Radial spotlight bottom-right */}
      <div className="bg-spot bg-spot-2" />

      {/* Mid accent */}
      <div className="bg-spot bg-spot-3" />

      {/* Dot grid overlay */}
      <div className="bg-dots" />

      {/* Horizontal scan lines – very subtle */}
      <div className="bg-lines" />

      {/* Noise grain */}
      <div className="bg-grain" />
    </div>
  );
}
