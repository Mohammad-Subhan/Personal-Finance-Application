import React from "react"
import { Plus } from "lucide-react"
import { FaWallet } from "react-icons/fa"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import DashboardChart from "@/components/DashboardChart"
import Layout from "@/components/Layout"
import { useNavigate } from 'react-router-dom'

const wallets = [
    "Wallet 1",
    "Wallet 2",
    "Wallet 3",
]

export default function DashboardPage() {
    const navigate = useNavigate()
    const [isDialogOpen, setIsDialogOpen] = React.useState(false)
    const [walletName, setWalletName] = React.useState("")
    const [selectedWallet, setSelectedWallet] = React.useState("")

    const handleSubmit = (e) => {
        e.preventDefault()
        console.log("Submitted:", { walletName, selectedWallet })
        setIsDialogOpen(false)
        // Here you would typically send this data to your backend or perform other actions
    }

    return (
        <Layout>
            <div className="container max-w-full p-6 mx-auto space-y-6">
                <div className="grid grid-cols-4 gap-4">
                    <Card className="col-span-1 p-4 bg-primaryAccent border-none text-background rounded-[35px]">
                        <div className="w-full h-full border-none bg-primary rounded-[22px] p-4">
                            <div className="space-y-1 h-4/5 w-4/5">
                                <h2 className="text-xl font-medium pb-[125px]">Mohammad Subhan Khalid</h2>
                                <div className="space-y-1">
                                    <p className="text-sm text-emerald-100">Wallets:</p>
                                    <p className="text-lg font-bold">3</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-sm text-emerald-100">Balance</p>
                                    <p className="text-3xl font-bold">Rs. 1740.00</p>
                                </div>
                            </div>
                        </div>
                    </Card>
                    <Card className="col-span-3 p-4">
                        <DashboardChart />
                    </Card>
                </div>

                <div className="flex justify-between items-center">
                    <h2 className="text-2xl font-semibold">Your Wallets</h2>
                    <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                        <DialogTrigger asChild>
                            <Button className="bg-primary hover:bg-primaryHover text-background">
                                <Plus className="w-4 h-4 mr-2" />
                                Add Wallet
                            </Button>
                        </DialogTrigger>
                        <DialogContent className="sm:max-w-[425px]">
                            <DialogHeader>
                                <DialogTitle>Add Wallet</DialogTitle>
                            </DialogHeader>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="walletName">Wallet Name</Label>
                                    <Input
                                        id="walletName"
                                        value={walletName}
                                        onChange={(e) => setWalletName(e.target.value)}
                                        placeholder="Enter wallet name"
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="walletType">Wallet Type</Label>
                                    <Select onValueChange={setSelectedWallet} value={selectedWallet}>
                                        <SelectTrigger id="walletType">
                                            <SelectValue placeholder="Select wallet type" />
                                        </SelectTrigger>
                                        <SelectContent className="bg-background">
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="bitcoin">Bitcoin</SelectItem>
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="ethereum">Ethereum</SelectItem>
                                            <SelectItem className="hover:cursor-pointer hover:bg-gray-50" value="litecoin">Litecoin</SelectItem>
                                        </SelectContent>
                                    </Select>
                                </div>
                                <Button type="submit" className="bg-primary hover:bg-primaryHover text-background">Save</Button>
                            </form>
                        </DialogContent>
                    </Dialog>
                </div>

                <div className="grid gap-4 md:grid-cols-3">
                    {wallets.map((wallet) => (
                        <Button key={wallet} variant="outline" onClick={() => navigate('/wallet')} className="h-28 bg-white drop-shadow-md hover:drop-shadow-xl border text-primary">
                            <FaWallet className="w-6 h-6 mr-2" />
                            <span>{wallet}</span>
                        </Button>
                    ))}
                </div>
            </div>
        </Layout>
    )
}