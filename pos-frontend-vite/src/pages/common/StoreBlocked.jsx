import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router'
import { logout } from '@/Redux Toolkit/features/user/userThunks'
import { clearStoreState } from '@/Redux Toolkit/features/store/storeSlice'
import { ThemeToggle } from '@/components/theme-toggle'
import { Button } from '@/components/ui/button'
import {
  Store,
  ShieldX,
  LogOut,
  Mail,
  User,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Circle,
} from 'lucide-react'

export default function StoreBlocked() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { userProfile } = useSelector((state) => state.user)
  const { store } = useSelector((state) => state.store)

  const handleLogout = async () => {
    await dispatch(logout())
    dispatch(clearStoreState())
    navigate('/auth/login')
  }

  const steps = [
    { label: 'Tạo tài khoản', done: true },
    { label: 'Điền thông tin cửa hàng', done: true },
    { label: 'Xét duyệt bởi Admin', done: false, failed: true },
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
            <div className="bg-destructive/10 border-b border-destructive/20 px-6 py-5 flex items-center gap-4">
              <div className="w-12 h-12 rounded-full bg-destructive/10 flex items-center justify-center flex-shrink-0">
                <ShieldX className="w-6 h-6 text-destructive" />
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-destructive mb-0.5">
                  Trạng thái tài khoản
                </p>
                <h1 className="text-xl font-bold text-foreground">
                  Yêu cầu bị từ chối
                </h1>
              </div>
              <span className="ml-auto inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-destructive/10 text-destructive text-xs font-semibold border border-destructive/20">
                <span className="w-1.5 h-1.5 rounded-full bg-destructive" />
                BLOCKED
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
                      ) : step.failed ? (
                        <XCircle className="w-5 h-5 text-destructive" />
                      ) : (
                        <Circle className="w-5 h-5 text-muted-foreground/40" />
                      )}
                    </div>
                    <span className={`text-sm ${step.done ? 'text-foreground font-medium' : step.failed ? 'text-destructive font-semibold' : 'text-muted-foreground'}`}>
                      {step.label}
                    </span>
                  </div>
                ))}
              </div>

              {/* Warning box */}
              <div className="flex items-start gap-3 p-3 rounded-lg bg-destructive/5 border border-destructive/20">
                <AlertTriangle className="w-4 h-4 text-destructive mt-0.5 flex-shrink-0" />
                <p className="text-xs text-muted-foreground leading-relaxed">
                  Yêu cầu đăng ký cửa hàng của bạn đã bị <strong className="text-destructive">từ chối hoặc khóa</strong> bởi Super Admin.
                  Vui lòng liên hệ hỗ trợ để biết thêm lý do và khiếu nại nếu cần.
                </p>
              </div>
            </div>

            {/* Footer actions */}
            <div className="px-6 py-4 bg-muted/30 border-t flex items-center gap-3">
              <Button
                variant="ghost"
                size="sm"
                className="gap-2 w-full text-muted-foreground"
                onClick={handleLogout}
              >
                <LogOut className="w-4 h-4" />
                Đăng xuất khỏi hệ thống
              </Button>
            </div>
          </div>

          {/* Help note */}
          <div className="flex items-start gap-3 px-4 py-3 rounded-xl border bg-card text-sm text-muted-foreground">
            <Mail className="w-4 h-4 mt-0.5 flex-shrink-0 text-primary" />
            <p>Nếu bạn cho rằng đây là nhầm lẫn, vui lòng liên hệ Admin hệ thống để được hỗ trợ.</p>
          </div>
        </div>
      </div>
    </div>
  )
}
