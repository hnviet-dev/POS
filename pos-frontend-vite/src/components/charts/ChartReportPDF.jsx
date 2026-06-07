import {
  Document,
  Page,
  Text,
  View,
  StyleSheet,
  Image,
} from "@react-pdf/renderer";

const styles = StyleSheet.create({
  page: {
    padding: 40,
    fontFamily: "Helvetica",
  },
  title: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 10,
    color: "#666666",
    marginBottom: 20,
  },
  chartImage: {
    width: "100%",
    maxHeight: 280,
    marginBottom: 20,
    objectFit: "contain",
  },
  table: {
    marginTop: 8,
  },
  headerRow: {
    flexDirection: "row",
    backgroundColor: "#f3f4f6",
    paddingVertical: 8,
    paddingHorizontal: 4,
  },
  row: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderBottomColor: "#e5e7eb",
    paddingVertical: 6,
    paddingHorizontal: 4,
  },
  headerCell: {
    flex: 1,
    fontSize: 10,
    fontWeight: "bold",
  },
  cell: {
    flex: 1,
    fontSize: 10,
  },
});

export const ChartReportPDF = ({
  title,
  generatedAt,
  columns,
  data,
  chartImage,
}) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.subtitle}>Generated: {generatedAt}</Text>
      {chartImage ? <Image style={styles.chartImage} src={chartImage} /> : null}
      <View style={styles.table}>
        <View style={styles.headerRow}>
          {columns.map((col) => (
            <Text key={col.key} style={styles.headerCell}>
              {col.label}
            </Text>
          ))}
        </View>
        {data.map((row, index) => (
          <View key={index} style={styles.row}>
            {columns.map((col) => (
              <Text key={col.key} style={styles.cell}>
                {String(row[col.key] ?? "")}
              </Text>
            ))}
          </View>
        ))}
      </View>
    </Page>
  </Document>
);
