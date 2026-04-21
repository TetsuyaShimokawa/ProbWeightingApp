export default function BlockBreakScreen({ onContinue }) {
  return (
    <div className="screen break-screen">
      <div className="break-content">
        <h2>前半が終了しました</h2>
        <p>お疲れ様でした。</p>
        <p>後半の実験を開始します。</p>
        <p>引き続きよろしくお願いします。</p>
        <button className="btn-primary" onClick={onContinue}>
          後半を始める
        </button>
      </div>
    </div>
  );
}
