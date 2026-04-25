import { AlertCircle } from "lucide-react";

export default function ErrorBox({ message }: { message: string }) {
  return (
    <div className="error-box" role="alert">
      <AlertCircle size={18} />
      <div>
        <p className="error-title">Failed to load</p>
        <p className="error-msg">{message}</p>
      </div>
    </div>
  );
}
