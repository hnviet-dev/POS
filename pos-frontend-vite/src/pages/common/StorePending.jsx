import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router'
import { logout } from '@/Redux Toolkit/features/user/userThunks'
import { clearStoreState } from '@/Redux Toolkit/features/store/storeSlice'
import { ThemeToggle } from '@/components/theme-toggle'
import { Button } from '@/components/ui/button'
import {
  Store,
  Clock,
  LogOut,
  RefreshCw,
  CheckCircle,
  Circle,
  AlertCircle,
  Mail,
  User,
} from 'lucide-react'

export default function StorePending() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { userProfile } = useSelector((state) => state.user)
  const { store } = useSelector((state) => state.store)

  const handleLogout = async () => {
    await dispatch(logout())
    dispatch(clearStoreState())
    navigate('/auth/login')
  }

  const handleRefresh = () => {
    window.location.reload()
  }

  const steps = [
    { label: 'Tạo tài khoản', done: true },
    { label: 'Điền thông tin cửa hàng', done: true },
    { label: 'Chờ Admin xét duyệt', done: false, active: true },
    { label: 'Kích hoạt & bắt đầu sử dụng', done: false },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 via-background to-primary/10 flex flex-col">
      {/* Topbar */}
      <header className="w-full h-16 bg-background border-b flex items-center px-6 justify-between shadow-sm">
        <div className="flex items-center gap-2 text-xl font-extrabold text-primary tracking-tight">
          <Store className="w-6 h-6 text-primary" />
          POS Admin
        </div>
        <div className="flex items-center gap-4">
          <ThemeToggle />
          <Button variant="outline" size="sm" onClick={handleLogout} className="gap-2 text-muted-foreground">
            <LogOut className="w-4 h-4" />
            Đăng xuất
          </Button>
        </div>
      </header>

      {/* Main content */}
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-lg space-y-6">

          {/* Status card */}
          <div className="bg-card border rounded-2xl shadow-xl overflow-hidden">
            {/* Header strip */}
            <div className="bg-amber-500/10 border-b border-amber-200 dark:border-amber-800 px-6 py-5 flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-900/40 flex items-center justify-center flex-shrink-0">
                <Clock className="w-6 h-6 text-amber-600 dark:text-amber-400 animate-pulse" />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-amber-600 dark:text-amber-400 mb-0.5">
                  Trạng thái tài khoản
                </p>
                <h1 className="text-xl font-bold text-foreground">
                  Đang chờ phê duyệt
                </h1>
              </div>
              <span className="ml-auto inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 dark:bg-amber-900/50 text-amber-700 dark:text-amber-300 text-xs font-semibold border border-amber-200 dark:border-amber-700">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
                PENDING
              </span>
            </div>

            {/* Body */}
            <div className="px-6 py-5 space-y-5">
              {/* Info user & store */}
              {(userProfile || store) && (
                <div className="grid grid-cols-2 gap-3">
                  {userProfile?.fullName && (
                    <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
                      <User className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-xs text-muted-foreground">Chủ cửa hàng</p>
                        <p className="text-sm font-medium text-foreground truncate">{userProfile.fullName}</p>
                      </div>
                    </div>
                  )}
                  {store?.brand && (
                    <div className="flex items-center gap-2 p-3 rounded-lg bg-muted/50">
                      <Store className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                      <div className="min-w-0">
                        <p className="text-xs text-muted-foreground">Cửa hàng</p>
                        <p className="text-sm font-medium text-foreground truncate">{store.brand}</p>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Progress steps */}
              <div className="space-y-2.5">
                <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Tiến trình</p>
                {steps.map((step, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="flex-shrink-0">
                      {step.done ? (
                        <CheckCircle className="w-5 h-5 text-primary" />
                      ) : step.active ? (
                        <AlertCircle className="w-5 h-5 text-amber-500 animate-pulse" />
                      ) : (
                        <Circle className="w-5 h-5 text-muted-foreground/40" />
                      )}
                    </div>
                    <span className={`text-sm ${step.done ? 'text-foreground font-medium' : step.active ? 'text-amber-600 dark:text-amber-400 font-semibold' : 'text-muted-foreground'}`}>
                      {step.label}
                    </span>
                  </div>
                ))}
              </div>

              <p className="text-xs text-muted-foreground leading-relaxed">
                Yêu cầu của bạn đã được ghi nhận. Admin sẽ xét duyệt trong vòng <strong className="text-foreground">1–2 ngày làm việc</strong>.
                Bạn sẽ có thể truy cập hệ thống sau khi được phê duyệt.
              </p>
            </div>

            {/* Footer actions */}
            <div className="px-6 py-4 bg-muted/30 border-t flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                className="gap-2 flex-1"
                onClick={handleRefresh}
              >
                <RefreshCw className="w-4 h-4" />
                Kiểm tra lại
              </Button>
              <Button
                variant="ghost"
                size="sm"
                className="gap-2 flex-1 text-muted-foreground"
                onClick={handleLogout}
              >
                <LogOut className="w-4 h-4" />
                Đăng xuất
              </Button>
            </div>
          </div>

          {/* Help note */}
          <div className="flex items-start gap-3 px-4 py-3 rounded-xl border bg-card text-sm text-muted-foreground">
            <Mail className="w-4 h-4 mt-0.5 flex-shrink-0 text-primary" />
            <p>Nếu bạn cần hỗ trợ, vui lòng liên hệ Admin hệ thống qua email.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
