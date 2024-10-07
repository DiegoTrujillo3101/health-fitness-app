// HomeScreen.js
import React from 'react';
import { View, Text, StyleSheet, Dimensions, TouchableOpacity } from 'react-native';

const { width, height } = Dimensions.get('window');

const HomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        {/* HeartRate Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('HeartRate')}>
          <Text style={styles.gridText}>Heart Rate</Text>
        </TouchableOpacity>

        {/* BloodPressure Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('BloodPressure')}>
          <Text style={styles.gridText}>Blood Pressure</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.row}>
        {/* Calorie Intake Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('CalorieTracker')}>
          <Text style={styles.gridText}>Calorie Intake</Text>
        </TouchableOpacity>

        {/* Water Intake Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('WaterTracker')}>
          <Text style={styles.gridText}>Water Intake</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.row}>
        {/* Workouts Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('Workouts')}>
          <Text style={styles.gridText}>Workouts</Text>
        </TouchableOpacity>

        {/* Summary Section */}
        <TouchableOpacity style={styles.gridItem} onPress={() => navigation.navigate('Summary')}>
          <Text style={styles.gridText}>Summary</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 10,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginVertical: 10,
  },
  gridItem: {
    flex: 1,
    height: height / 4 - 20,
    backgroundColor: '#4CAF50',
    justifyContent: 'flex-start',
    alignItems: 'center',
    marginHorizontal: 5,
    borderRadius: 15,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 5,
  },
  gridText: {
    color: '#ffffff',
    fontSize: 20,
    fontWeight: '600',
    position: 'absolute',
    top: 15,
  },
});

export default HomeScreen;
