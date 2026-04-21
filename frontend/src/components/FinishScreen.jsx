import { getCsvUrl } from "../api/client";

export default function FinishScreen({ studentId }) {
  const csvUrl = getCsvUrl(studentId);

  return (
    <div className="screen finish-screen">
      <div className="finish-content">
        <h2>実験が終了しました</h2>
        <p>ご協力ありがとうございました。</p>
        <a
          href={csvUrl}
          download
          className="btn-primary btn-download"
        >
          結果をCSVでダウンロード
        </a>
      </div>
    </div>
  );
}
