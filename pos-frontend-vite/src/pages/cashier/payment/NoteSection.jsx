import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { selectNote, setNote } from "../../../Redux Toolkit/features/cart/cartSlice";
import { FileText } from "lucide-react";

const NoteSection = () => {
  const dispatch = useDispatch();
  const note = useSelector(selectNote);

  return (
    <div className="p-4 border-b">
      <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3 flex items-center gap-1.5">
        <FileText className="w-3.5 h-3.5" />
        Ghi chú đơn hàng
      </h2>
      <textarea
        className="w-full px-3 py-2 rounded-lg border bg-background text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary/30 placeholder:text-muted-foreground/60 transition"
        rows={3}
        placeholder="Thêm ghi chú cho đơn hàng..."
        value={note}
        onChange={(e) => dispatch(setNote(e.target.value))}
      />
    </div>
  );
};

export default NoteSection;
