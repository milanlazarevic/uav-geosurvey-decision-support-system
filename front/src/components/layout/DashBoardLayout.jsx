export default function DashboardLayout({ left, center, right }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 h-screen">
      {/* <div className="bg-black">{left}</div> */}
      <div className="bg-black">{center}</div>
      <div className="bg-black overflow-auto">{right}</div>
    </div>
  );
}
