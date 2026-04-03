import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { GoogleIcon, MailIcon, LockIcon, UserIcon, PhoneIcon, EyeIcon, ArrowRightIcon } from "./icons/AuthIcons";
import "./auth.css";
import axios from "axios";

function getPasswordStrength(pw) {
  if (!pw) return 0;
  let s = 0;
  if (pw.length >= 8) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  return s;
}

export default function SignupPage() {
  const navigate = useNavigate(); 
  const [showPw, setShowPw] = useState(false);
  const [form, setForm] = useState({ name: "", email: "", phone: "", password: "" });
  const strength = getPasswordStrength(form.password);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const strengthClass = (i) => {
    if (i >= strength) return "";
    if (strength === 1) return "active-weak";
    if (strength <= 2) return "active-medium";
    return "active-strong";
  };

  const handleSubmit = async () => {
    
    // Basic Validation Check
    if (!form.name || !form.email || !form.phone || !form.password){
        setError("Please fill in all fields.");
        return;
    }

    // Password Check
    if (form.password.length < 8){
        setError("Password must be at least 8 characters.");
        return;
    }

    try{
        
        setLoading(true);
        setError("");

        const response = await axios.post("https://authify-jtr3.onrender.com/api/v1/auth/user", {
            username: form.name,
            email: form.email,
            phone: form.phone,
            password: form.password
        });
        console.log(response.status);
        navigate("/login");

    } catch (err){

        const message = err.response?.data?.message || "Signup failed. Try again.";
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

        <h1 className="auth-heading">Create account</h1>
        <p className="auth-sub">Join us — it only takes a minute</p>

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
          <label className="field-label">Full name</label>
          <div className="field-wrap">
            <span className="field-icon"><UserIcon /></span>
            <input
              className="field-input"
              type="text"
              placeholder="John Doe"
              value={form.name}
              onChange={e => setForm(f => ({ ...f, name: e.target.value }))}
            />
          </div>
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
          <label className="field-label">Phone number</label>
          <div className="field-wrap">
            <span className="field-icon"><PhoneIcon /></span>
            <input
              className="field-input"
              type="tel"
              placeholder="+1 (555) 000-0000"
              value={form.phone}
              onChange={e => setForm(f => ({ ...f, phone: e.target.value }))}
            />
          </div>
        </div>

        <div className="field-group" style={{ marginBottom: 10 }}>
          <label className="field-label">Password</label>
          <div className="field-wrap">
            <span className="field-icon"><LockIcon /></span>
            <input
              className="field-input has-right-icon"
              type={showPw ? "text" : "password"}
              placeholder="Create a strong password"
              value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
            />
            <button className="field-eye" onClick={() => setShowPw(v => !v)} type="button">
              <EyeIcon open={showPw} />
            </button>
          </div>
          {form.password && (
            <div className="strength-row">
              {[0,1,2,3].map(i => (
                <div key={i} className={`strength-bar ${strengthClass(i)}`} />
              ))}
            </div>
          )}
        </div>

        <div style={{ marginBottom: 24 }} />

        <p className="terms-text">
          By creating an account, you agree to our{" "}
          <a>Terms of Service</a> and <a>Privacy Policy</a>
        </p>

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
          {loading ? "Creating account..." : <> Create account <ArrowRightIcon /> </>}
        </button>

        <p className="switch-text">
          Already have an account?{" "}
          <span className="switch-link" onClick={() => navigate("/login")}>  {/* ← CHANGE */}
            Sign in
          </span>
        </p>
      </div>
    </div>
  );
}