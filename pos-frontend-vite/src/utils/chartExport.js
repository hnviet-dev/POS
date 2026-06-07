function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function escapeCsvValue(value) {
  const str = String(value ?? "");
  if (str.includes(",") || str.includes('"') || str.includes("\n")) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

export function slugifyFilename(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

export function downloadCsv(data, columns, filename) {
  const header = columns.map((col) => escapeCsvValue(col.label)).join(",");
  const rows = data.map((row) =>
    columns.map((col) => escapeCsvValue(row[col.key])).join(","),
  );
  const csv = [header, ...rows].join("\n");
  const blob = new Blob(["\ufeff" + csv], {
    type: "text/csv;charset=utf-8;",
  });
  triggerDownload(blob, `${filename}.csv`);
}

async function svgToCanvas(svgElement) {
  const bbox = svgElement.getBoundingClientRect();
  const width = Math.max(bbox.width, 400);
  const height = Math.max(bbox.height, 250);

  const svgClone = svgElement.cloneNode(true);
  svgClone.setAttribute("xmlns", "http://www.w3.org/2000/svg");
  svgClone.setAttribute("width", width);
  svgClone.setAttribute("height", height);

  const svgData = new XMLSerializer().serializeToString(svgClone);
  const svgBlob = new Blob([svgData], {
    type: "image/svg+xml;charset=utf-8",
  });
  const url = URL.createObjectURL(svgBlob);

  const img = new Image();
  await new Promise((resolve, reject) => {
    img.onload = resolve;
    img.onerror = reject;
    img.src = url;
  });

  const scale = 2;
  const canvas = document.createElement("canvas");
  canvas.width = width * scale;
  canvas.height = height * scale;
  const ctx = canvas.getContext("2d");
  ctx.scale(scale, scale);
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, width, height);
  ctx.drawImage(img, 0, 0, width, height);
  URL.revokeObjectURL(url);

  return canvas;
}

export async function chartRefToBase64(chartRef) {
  const svg = chartRef?.current?.querySelector("svg");
  if (!svg) return null;
  const canvas = await svgToCanvas(svg);
  return canvas.toDataURL("image/png");
}

export async function downloadChartPng(chartRef, filename) {
  const svg = chartRef?.current?.querySelector("svg");
  if (!svg) {
    throw new Error("Chart not found");
  }
  const canvas = await svgToCanvas(svg);
  await new Promise((resolve, reject) => {
    canvas.toBlob((blob) => {
      if (!blob) {
        reject(new Error("Failed to generate PNG"));
        return;
      }
      triggerDownload(blob, `${filename}.png`);
      resolve();
    }, "image/png");
  });
}
