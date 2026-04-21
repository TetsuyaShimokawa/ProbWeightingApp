import ProgressBar from "./ProgressBar";

export default function Step4Screen({ trial, stepData, trialIndex, totalTrials, onNext, loading }) {
  const { r, x_prime, N, block } = trial;
  const { s, y_prime } = stepData;
  const rN = (r ** N).toFixed(3);
  const sN = (s ** N).toFixed(3);
  const trialNum = trialIndex + 1;

  return (
    <div className="screen">
      <ProgressBar current={trialNum} total={totalTrials} block={block} N={N} />

      <div className="step-label">Step 4</div>

      <p className="question-intro">以下の2つのくじを比べてください：</p>

      <div className="lottery-compare">
        <div className="lottery-box lottery-x">
          <div className="lottery-label">X</div>
          <div className="lottery-detail">
            確率 <strong>{rN}</strong> で
          </div>
          <div className="lottery-amount">{x_prime}円</div>
        </div>

        <div className="vs-label">vs</div>

        <div className="lottery-box lottery-y">
          <div className="lottery-label">Y</div>
          <div className="lottery-detail">
            確率 <strong>{sN}</strong> で
          </div>
          <div className="lottery-amount">{y_prime}円</div>
        </div>
      </div>

      <div className="choice-buttons">
        <button
          className="btn-choice btn-x"
          onClick={() => onNext("X")}
          disabled={loading}
        >
          Xを好む
        </button>
        <button
          className="btn-choice btn-indifferent"
          onClick={() => onNext("Indifferent")}
          disabled={loading}
        >
          ほとんど無差別
        </button>
        <button
          className="btn-choice btn-y"
          onClick={() => onNext("Y")}
          disabled={loading}
        >
          Yを好む
        </button>
      </div>

      {loading && <p className="saving">保存中...</p>}
    </div>
  );
}
