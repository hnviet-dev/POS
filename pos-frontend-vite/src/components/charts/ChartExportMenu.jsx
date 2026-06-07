import React, { useState } from "react";
import { Download, FileSpreadsheet, FileText, ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { useToast } from "@/components/ui/use-toast";
import {
  downloadCsv,
  downloadChartPng,
  slugifyFilename,
} from "@/utils/chartExport";
import { downloadChartPdf } from "@/utils/chartExportPdf";

const ChartExportMenu = ({
  chartRef,
  title,
  data = [],
  columns = [],
  disabled = false,
  size = "sm",
}) => {
  const { toast } = useToast();
  const [exporting, setExporting] = useState(false);

  const handleExport = async (format) => {
    if (!data.length) {
      toast({
        title: "No data",
        description: "There is no chart data to export.",
        variant: "destructive",
      });
      return;
    }

    const filename = `${slugifyFilename(title)}-${Date.now()}`;

    try {
      setExporting(true);

      if (format === "csv") {
        downloadCsv(data, columns, filename);
      } else if (format === "png") {
        await downloadChartPng(chartRef, filename);
      } else if (format === "pdf") {
        await downloadChartPdf({
          title,
          data,
          columns,
          chartRef,
          filename,
        });
      }

      toast({
        title: "Export successful",
        description: `${title} exported as ${format.toUpperCase()}.`,
      });
    } catch (error) {
      console.error("Chart export error:", error);
      toast({
        title: "Export failed",
        description: error.message || "Could not export chart. Please try again.",
        variant: "destructive",
      });
    } finally {
      setExporting(false);
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline" size={size} disabled={disabled || exporting}>
          <Download className="h-4 w-4 mr-1" />
          {exporting ? "Exporting..." : "Export"}
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => handleExport("png")}>
          <ImageIcon className="h-4 w-4 mr-2" />
          PNG Image
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport("csv")}>
          <FileSpreadsheet className="h-4 w-4 mr-2" />
          CSV Data
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleExport("pdf")}>
          <FileText className="h-4 w-4 mr-2" />
          PDF Report
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

export default ChartExportMenu;
