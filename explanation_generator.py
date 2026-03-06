{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "398ed05e-7b9e-4e6d-a2d1-6dfb5eb7bda2",
   "metadata": {},
   "outputs": [],
   "source": [
    "def generate_explanation(row):\n",
    "\n",
    "    reasons = []\n",
    "\n",
    "    # weight mismatch\n",
    "    if row[\"weight_diff\"] > 500:\n",
    "        reasons.append(\"Large mismatch between declared and measured weight\")\n",
    "\n",
    "    # suspicious value/weight\n",
    "    if row[\"value_per_weight\"] > 1000:\n",
    "        reasons.append(\"Unusual value-to-weight ratio\")\n",
    "\n",
    "    # dwell time anomaly\n",
    "    if row[\"long_dwell\"] == 1:\n",
    "        reasons.append(\"Container stayed unusually long at port\")\n",
    "\n",
    "    # anomaly detection\n",
    "    if row[\"Anomaly_Flag\"] == 1:\n",
    "        reasons.append(\"Shipment pattern deviates from normal trade behavior\")\n",
    "\n",
    "    # if nothing suspicious\n",
    "    if len(reasons) == 0:\n",
    "        return \"Shipment appears normal with no significant anomalies\"\n",
    "\n",
    "    return \", \".join(reasons)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9a0910c8-68b6-47b8-a4d7-51e232e1bb8a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
