import { pdf } from "@react-pdf/renderer";
import { ChartReportPDF } from "@/components/charts/ChartReportPDF";
import { chartRefToBase64 } from "@/utils/chartExport";

export async function downloadChartPdf({
  title,
  data,
  columns,
  chartRef,
  filename,
}) {
  const chartImage = chartRef ? await chartRefToBase64(chartRef) : null;
  const generatedAt = new Date().toLocaleString();
  const pdfDoc = pdf(
    <ChartReportPDF
      title={title}
      generatedAt={generatedAt}
      columns={columns}
      data={data}
      chartImage={chartImage}
    />,
  );
  const blob = await pdfDoc.toBlob();

  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${filename}.pdf`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
