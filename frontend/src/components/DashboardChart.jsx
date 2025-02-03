import { Bar, BarChart, XAxis } from "recharts"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const chartData = [
    { month: "January", desktop: 186, mobile: 80 },
    { month: "February", desktop: 305, mobile: 200 },
    { month: "March", desktop: 237, mobile: 120 },
    { month: "April", desktop: 73, mobile: 190 },
    { month: "May", desktop: 209, mobile: 130 },
    { month: "June", desktop: 214, mobile: 140 },
]

const chartConfig = {
    desktop: {
        label: "Desktop",
        color: "#2563eb",
    },
    mobile: {
        label: "Mobile",
        color: "#60a5fa",
    },
}

function DashboardChart() {
    return (
        <div className="w-full max-w-[600px] mx-auto">
            <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
                <BarChart
                    width={600}  // Ensures the max width is respected
                    height={300}
                    data={chartData}
                >
                    <XAxis
                        dataKey="month"
                        tickLine={false}
                        tickMargin={10}
                        axisLine={false}
                        tickFormatter={(value) => value.slice(0, 3)}
                    />
                    <ChartTooltip content={<ChartTooltipContent />} />
                    <Bar dataKey="desktop" fill={chartConfig.desktop.color} radius={4} />
                    <Bar dataKey="mobile" fill={chartConfig.mobile.color} radius={4} />
                </BarChart>
            </ChartContainer>
        </div>
    )
}

export default DashboardChart;