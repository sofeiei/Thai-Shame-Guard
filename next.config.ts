import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // นำลิงก์ที่ได้จาก Render มาใส่ตรงนี้ครับ (อย่าลืมใส่ https:// นำหน้า)
        destination: 'https://thai-shame-guard.onrender.com/:path*', 
      },
    ]
  },
};

export default nextConfig;
