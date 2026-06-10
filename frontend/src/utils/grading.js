export function calculateGrade(utuh, pecah, bendaAsing, basePrice = 0) {
  // Hitung persentase butir utuh dari SEMUA objek terdeteksi (termasuk benda asing)
  // agar grade tidak bisa PREMIUM meski ada banyak benda asing
  const total = utuh + pecah + bendaAsing
  const percentUtuh = total === 0 ? 0 : (utuh / total) * 100

  let grade, label, description, colorClass, barColor, finalPrice

  if (percentUtuh >= 85) {
    grade       = 'PREMIUM'
    label       = 'LOLOS QC — GRADE A'
    description = 'Kualitas beras sangat baik, dominan butir utuh.'
    colorClass  = 'grade-premium'
    barColor    = '#7EA86A'
    finalPrice  = basePrice
  } else {
    grade       = 'MEDIUM'
    label       = 'LOLOS QC — GRADE B'
    description = 'Kualitas standar, terdapat patahan yang wajar.'
    colorClass  = 'grade-medium'
    barColor    = '#C07558'
    finalPrice  = basePrice * 0.9
  }

  if (bendaAsing > 2) {
    grade       = 'TIDAK BERSIH'
    label       = 'TIDAK LAYAK KONSUMSI'
    description = 'Terlalu banyak benda asing — tidak aman dikonsumsi.'
    colorClass  = 'grade-dirty'
    barColor    = '#8B2020'
    finalPrice  = 0
  } else if (bendaAsing > 0) {
    grade       = 'LOW'
    label       = 'REJECT — PERLU SORTIR ULANG'
    description = 'Terdeteksi benda asing, perlu dibersihkan lebih lanjut.'
    colorClass  = 'grade-low'
    barColor    = '#D9534F'
    finalPrice  = finalPrice * 0.8
  }

  return {
    grade,
    label,
    description,
    colorClass,
    barColor,
    percentUtuh: parseFloat(percentUtuh.toFixed(1)),
    finalPrice: Math.floor(finalPrice),
    formattedPrice: 'Rp ' + Math.floor(finalPrice).toLocaleString('id-ID'),
  }
}
