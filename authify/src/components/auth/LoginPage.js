import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleIcon, MailIcon, LockIcon, EyeIcon, ArrowRightIcon, CheckIcon } from "./icons/AuthIcons";
import "./auth.css";
import axios from "axios";

export default function LoginPage() {
  const navigate = useNavigate(); 
  const [showPw, setShowPw] = useState(false);
  const [checked, setChecked] = useState(false);
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    // Basic Validation Check
    if (!form.email || !form.password){
        setError("Please fill in all fileds.");
        return;
    }

    try {

        setLoading(true);
        setError("");

        // Response
        const response = await axios.post("https://authify-backend-zcmx.onrender.com/api/v1/auth/login", {
            email: form.email,
            password: form.password,
        });

        // Extracting Token
        const access_token = response.data.user_data.access_token;
        const refresh_token = response.data.user_data.refresh_token;

        // storing in Browser Local Storage
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);

        // Redirect 
        navigate("/signup");

    } catch(err){
        const message = err.response?.data?.message || "Login failed. Try again.";
        setError(message);
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="auth-root">
      <div className="grid-overlay" />
      <div className="auth-card">
        <div className="brand">
          <div className="brand-mark">A</div>
          <span className="brand-name">Authify</span>
        </div>

        <h1 className="auth-heading">Welcome back</h1>
        <p className="auth-sub">Sign in to continue to your account</p>

        <div className="social-row">
          <button className="social-btn">
            <GoogleIcon /> Continue with Google
          </button>
        </div>

        <div className="divider">
          <div className="divider-line" />
          <span className="divider-text">or</span>
          <div className="divider-line" />
        </div>

        <div className="field-group">
          <label className="field-label">Email address</label>
          <div className="field-wrap">
            <span className="field-icon"><MailIcon /></span>
            <input
              className="field-input"
              type="email"
              placeholder="hello@example.com"
              value={form.email}
              onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
            />
          </div>
        </div>

        <div className="field-group">
          <label className="field-label">Password</label>
          <div className="field-wrap">
            <span className="field-icon"><LockIcon /></span>
            <input
              className="field-input has-right-icon"
              type={showPw ? "text" : "password"}
              placeholder="Enter your password"
              value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
            />
            <button className="field-eye" onClick={() => setShowPw(v => !v)} type="button">
              <EyeIcon open={showPw} />
            </button>
          </div>
        </div>

        <div className="row-flex">
          <label className="remember-label" onClick={() => setChecked(v => !v)}>
            <div className={`custom-checkbox${checked ? " checked" : ""}`}>
              {checked && <CheckIcon />}
            </div>
            Remember me
          </label>
          <span className="forgot-link">Forgot password?</span>
        </div>

        {/* 6️⃣ Show error if any */}
        {error && (
          <p style={{
            color: "#ef4444",
            fontSize: "13px",
            marginBottom: "16px",
            textAlign: "center"
          }}>
            {error}
          </p>
        )}
        
        {/* 7️⃣ Button shows loading state */}
        <button
          className="submit-btn"
          onClick={handleSubmit}
          disabled={loading}
          style={{ opacity: loading ? 0.7 : 1 }}
        >
          {loading ? "Signing in..." : <> Sign in <ArrowRightIcon /> </>}
        </button>

        <p className="switch-text">
          Don't have an account?{" "}
          <span className="switch-link" onClick={() => navigate("/signup")}>  {/* ← CHANGE */}
            Create one
          </span>
        </p>
      </div>
    </div>
  );
}