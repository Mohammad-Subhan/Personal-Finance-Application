import { TopNav } from "@/components/TopNav"

export default function Layout({ children }) {
    return (
        <>
            <TopNav />
            <main className="min-h-screen">{children}</main>
        </>
    )
}