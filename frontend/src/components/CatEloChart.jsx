import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { formatShortDate } from '../lib/format.js';
import { CHART_COLORS } from '../lib/chartColors.js';
import './CatEloChart.css';

function CatEloChart({ history }) {
  const chartData = history.map((game) => ({
    date: formatShortDate(game.date),
    catelo: Math.round(game.catelo),
  }));

  return (
    <div className="chart-container">
      <h2>CatElo Rating Over Time</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.grid} />
          <XAxis
            dataKey="date"
            stroke={CHART_COLORS.text}
            tick={{ fill: CHART_COLORS.text }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis
            stroke={CHART_COLORS.text}
            tick={{ fill: CHART_COLORS.text }}
            domain={['dataMin - 50', 'dataMax + 50']}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: CHART_COLORS.tooltipBackground,
              border: `1px solid ${CHART_COLORS.text}`,
              color: CHART_COLORS.text,
            }}
            labelStyle={{ color: CHART_COLORS.accent }}
          />
          <Line
            type="monotone"
            dataKey="catelo"
            stroke={CHART_COLORS.accent}
            strokeWidth={2}
            dot={{ fill: CHART_COLORS.accent, r: 3 }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default CatEloChart;
