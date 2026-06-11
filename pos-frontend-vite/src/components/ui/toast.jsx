import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"
import { cva } from "class-variance-authority"
import { X, CheckCircle2, XCircle, AlertTriangle, Info, Bell } from "lucide-react"

import { cn } from "@/lib/utils"

const ToastProvider = ToastPrimitives.Provider

const ToastViewport = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "fixed top-4 right-4 z-[100] flex max-h-screen w-full flex-col gap-2 sm:max-w-[400px]",
      className
    )}
    {...props}
  />
))
ToastViewport.displayName = ToastPrimitives.Viewport.displayName

const toastVariants = cva(
  [
    "group pointer-events-auto relative flex w-full items-start gap-3 overflow-hidden rounded-xl border p-4 shadow-2xl",
    "transition-all duration-300",
    "data-[state=open]:animate-in data-[state=open]:slide-in-from-right-full data-[state=open]:fade-in-0",
    "data-[state=closed]:animate-out data-[state=closed]:slide-out-to-right-full data-[state=closed]:fade-out-0",
    "data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)]",
    "data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none",
  ].join(" "),
  {
    variants: {
      variant: {
        default:
          "border-border/50 bg-background/95 backdrop-blur-md text-foreground",
        destructive:
          "border-red-500/30 bg-red-950/90 backdrop-blur-md text-red-50",
        success:
          "border-emerald-500/30 bg-emerald-950/90 backdrop-blur-md text-emerald-50",
        warning:
          "border-amber-500/30 bg-amber-950/90 backdrop-blur-md text-amber-50",
        info:
          "border-blue-500/30 bg-blue-950/90 backdrop-blur-md text-blue-50",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const toastIcons = {
  default:     <Bell         className="h-5 w-5 text-muted-foreground mt-0.5 flex-shrink-0" />,
  destructive: <XCircle      className="h-5 w-5 text-red-400        mt-0.5 flex-shrink-0" />,
  success:     <CheckCircle2 className="h-5 w-5 text-emerald-400    mt-0.5 flex-shrink-0" />,
  warning:     <AlertTriangle className="h-5 w-5 text-amber-400     mt-0.5 flex-shrink-0" />,
  info:        <Info         className="h-5 w-5 text-blue-400       mt-0.5 flex-shrink-0" />,
}

const toastAccent = {
  default:     "bg-border",
  destructive: "bg-red-500",
  success:     "bg-emerald-500",
  warning:     "bg-amber-500",
  info:        "bg-blue-500",
}

const Toast = React.forwardRef(({ className, variant = "default", children, ...props }, ref) => {
  return (
    <ToastPrimitives.Root
      ref={ref}
      className={cn(toastVariants({ variant }), className)}
      {...props}
    >
      {/* Thanh accent bên trái */}
      <span
        className={cn(
          "absolute left-0 top-0 h-full w-1 rounded-l-xl",
          toastAccent[variant] || toastAccent.default
        )}
      />
      {/* Icon */}
      {toastIcons[variant] || toastIcons.default}
      {/* Nội dung */}
      <div className="flex-1 min-w-0 ml-1">
        {children}
      </div>
    </ToastPrimitives.Root>
  )
})
Toast.displayName = ToastPrimitives.Root.displayName

const ToastAction = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Action
    ref={ref}
    className={cn(
      "inline-flex h-8 shrink-0 items-center justify-center rounded-lg border border-white/20 bg-white/10 px-3 text-xs font-medium",
      "transition-colors hover:bg-white/20 focus:outline-none focus:ring-1 focus:ring-white/30",
      "disabled:pointer-events-none disabled:opacity-50",
      className
    )}
    {...props}
  />
))
ToastAction.displayName = ToastPrimitives.Action.displayName

const ToastClose = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Close
    ref={ref}
    className={cn(
      "absolute right-2 top-2 rounded-md p-1",
      "text-foreground/30 opacity-0 transition-all",
      "hover:text-foreground hover:bg-white/10",
      "focus:opacity-100 focus:outline-none",
      "group-hover:opacity-100",
      className
    )}
    toast-close=""
    {...props}
  >
    <X className="h-3.5 w-3.5" />
  </ToastPrimitives.Close>
))
ToastClose.displayName = ToastPrimitives.Close.displayName

const ToastTitle = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Title
    ref={ref}
    className={cn("text-sm font-semibold leading-tight tracking-tight", className)}
    {...props}
  />
))
ToastTitle.displayName = ToastPrimitives.Title.displayName

const ToastDescription = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Description
    ref={ref}
    className={cn("text-xs opacity-80 mt-0.5 leading-relaxed", className)}
    {...props}
  />
))
ToastDescription.displayName = ToastPrimitives.Description.displayName

export {
  ToastProvider,
  ToastViewport,
  Toast,
  ToastTitle,
  ToastDescription,
  ToastClose,
  ToastAction,
}