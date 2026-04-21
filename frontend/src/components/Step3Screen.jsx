import { useState } from "react";
import ProgressBar from "./ProgressBar";

export default function Step3Screen({ trial, trialIndex, totalTrials, onNext }) {
  const [yPrime, setYPrime] = useState("");
  const [validationError, setValidationError] = useState("");

  const { p, q, x_prime, N, block } = trial;
  const pN = (p ** N).toFixed(3);
  const qN = (q ** N).toFixed(3);
  const trialNum = trialIndex + 1;

  function handleSubmit(e) {
    e.preventDefault();
    const val = parseFloat(yPrime);
    if (isNaN(val) || val < 1 || val > 100_000_000 || !Number.isFinite(val)) {
      setValidationError("1〜100,000,000 の数値を入力してください");
      return;
    }
    setValidationError("");
    onNext(val);
  }

  return (
    <div className="screen">
      <ProgressBar current={trialNum} total={totalTrials} block={block} N={N} />

      <div className="step-label">Step 3</div>

      <div className="question-box">
        <p>
          <strong>（確率 {pN} で {x_prime}円）</strong> と無差別になる
        </p>
        <p>
          <strong>（確率 {qN} で <span className="unknown">?円</span>）</strong> を答えてください
        </p>
        <p className="hint">※ 確率は p^{N} と q^{N} の値です</p>
      </div>

      <form onSubmit={handleSubmit} className="input-form">
        <div className="field">
          <label htmlFor="yPrime">金額 y'（円）</label>
          <input
            id="yPrime"
            type="number"
            min="1"
            max="100000000"
            step="any"
            value={yPrime}
            onChange={(e) => setYPrime(e.target.value)}
            placeholder="例：30"
            autoFocus
          />
        </div>
        {validationError && <p className="error">{validationError}</p>}
        <button type="submit" className="btn-primary">次へ</button>
      </form>
    </div>
  );
}
